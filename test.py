from lib import *
import collections, secrets
runs = []
for _ in range(10):
    print(gen_primes())
for _ in range(10):
    print(gen_pseudoprime())

for _ in range(10):
    key = rsa_gen_keys()
    t = secrets.randbits(100)
    print(t == rsa_decrypt(key[0], key[4], rsa_encrypt(key[0], key[3], t)))