from lib import *
import collections
runs = []
for _ in range(10000):
    runs.append(len(gen_primes().keys()))

counter=collections.Counter(runs)
print(counter)