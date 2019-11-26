"""Шифрование и дешифрование по RSA.
Проектное домашнее задание по алгебре,
бакалавриат «Современное программирование»
факультета Математики и компьютерных наук СПбГУ"""

import secrets
from math import log, ceil, gcd

def gen_divs(primes):
    low = 2**123
    high = 2**128

    m = 2
    divs = {2 : 1}
    step = 2
    
    while (m < low):
        p = secrets.choice(list(filter(lambda x : 1 if x*m < high  else 0, primes)))
        if (step <= 5 and p in divs.keys()) : continue
        deg = secrets.choice(range(1, min(step, ceil(128*log(2, p) - log(m, p)))))
        m *= p**deg
        if p not in divs.keys():
            divs[p] = deg
        else:
            divs[p] += deg
        step += 1

    return m, divs

def gen_primes():
    """Генерация доказуемо простых на основе теста Люка.

    Возвращает кортеж (n, ps, a), где
    n — простое между 2^123 и 2^128;
    ps — список простых, на которые раскладывается n-1;
    a — число, удовлетворяющее тесту Люка."""

    numbers = [x for x in range(2, 129)]
    is_prime = [True]*127
    for x in numbers:
        for i in range(2*x, 129, x):
            is_prime[i-2] = False
    primes = []
    for i, x in enumerate(is_prime):
        if x:
            primes.append(numbers[i])

    found = False

    while not found:
        
        m, divs = gen_divs(primes)

        n = m + 1
        for a in range(2, int(log(n, 2) + 1)):
            if pow(a, n-1, n) != 1: break
            for p in divs.keys():
                if pow(a, (n-1)//p, n) != 1:
                    found = True
                    return (n, divs.keys(), a)
        
def miller_rabin(n):
    if n % 2 == 0 : return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(int(log(n, 2) + 1)):
        a = secrets.randbits(129) % n
        t = pow(a, d, n)
        if t == 1 : continue
        for _ in range(s):
            t2 = pow(t, 2, n)
            if t2 == 1:
                if t != n-1:
                    return False
                t = t2
                break
            t = t2
        if t != 1:
            return False
    
    return True


def gen_pseudoprime():
    """Генерация псевдопростых на основе теста Миллера—Рабина.

    Возвращает целое число n в диапазоне от 2^123 до 2^128,
    псевдопростое по основание не менее чем log(n) чисел."""

    while True:
        bits = secrets.choice(range(123, 129))
        n = secrets.randbits(bits)
        
        if miller_rabin(n):
            return n
        
def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def mulinv(a, b):
    """return x such that (x * a) % b == 1"""
    g, x, _ = xgcd(a, b)
    if g == 1:
        return x % b

def rsa_gen_keys():
    """Генерация открытого и секретного ключей.

    Возвращает кортеж (n, p, q, e, d), где
    n = p*q;
    p, q — сильно псевдопростые по не менее чем log(q) основаниям;
    e — целое число, меньшее n и взаимно простое с phi(n), значением функции Эйлера от n,
    d — целое число, обратное к e по модулю phi(n)."""

    p = gen_pseudoprime()
    q = gen_pseudoprime()
    phi = (p-1)*(q-1)
    n = p*q
    e = secrets.randbits(32 + secrets.randbelow(64))
    while gcd(e, phi) != 1:
        e = secrets.randbits(32 + secrets.randbelow(64))

    d = mulinv(e, phi)

    return (n, p, q, e, d)


def rsa_encrypt(n, e, t):
    """Шифрование по RSA.

    На входе открытый ключ n, e и сообщение t.
    Возвращает целое число, равное t^e mod n."""
    return pow(t, e, n)


def rsa_decrypt(n, d, s):
    """Дешифрование по RSA.

    На входе закрытый ключ n, d и зашифрованное сообщение s.
    Возвращает целое число, равное s^d mod n."""
    return pow(s, d, n)


def fast_pow_mod(n, a, d):
    """Быстрое возведение в степень по модулю.

    Возвращает a^d mod n."""
    pass


def prime_factorization_pollard(n, cutoff):
    """Разложение на простые по алгоритму Полларда.

    На входе целое число n (имеющие вид p*q для некоторых простых p, q)
    и константа отсечения cutoff ~ log(n).
    Возвращает нетривиальный делитель p (или 1, если найти такой не удалось)."""
    pass