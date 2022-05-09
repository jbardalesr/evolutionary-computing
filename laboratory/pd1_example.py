import matplotlib.pyplot as plt
import numpy as np
import math
import random


class People:
    def __init__(self, low, high, eps) -> None:
        self.low = low
        self.high = high
        self.eps = eps
        # max iter number in accord to eps
        self.n = round((high - low)/eps) + 1
        self.l = int(math.log2(self.n) + 1)
        print(self.l)

    def encrypt(self, x: int):
        return x ^ (x >> 1)

    def decrypt(self, x: int):
        mask = x
        while mask:
            mask >>= 1
            x ^= mask
        return x

    def gen(self, fen):
        return self.encrypt(round((fen - self.low)/self.eps))

    def fen(self, gen):
        return self.decrypt(gen)*self.eps + self.low

    def get_random_fen(self):
        return random.randint(0, self.n - 1)*self.eps + self.low

    def get_random_gen(self):
        return self.encrypt(self.get_random_gen())


MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.85
N = 20
ITER = 200
people = People(0, 5, 1e-3)


def f(x):
    return -x*(math.sin(x) + math.cos(5*x))


def mutation(p):
    if random.random() <= MUTATION_RATE:
        i = random.randint(0, people.l - 1)
        p = min(people.high, people.fen(people.gen(p) ^ (1 << i)))
    return p


def crossover(p, q):
    new_p = p
    if random.random() < CROSSOVER_RATE:
        i = random.randint(0, people.l - 1)
        l = people.gen(p) & ((1 << i) - 1)
        r = (people.gen(q) >> i) << i
        new_p = people.fen(l | r)
    return new_p


def fitness(F):
    return F - np.min(F) + 1e-3


def select(pop, fitness):
    idx = np.random.choice(np.arange(N), size=N, replace=True, p=fitness/fitness.sum())
    return pop[idx]


pop = np.array([people.get_random_fen() for _ in range(N)])
best = []
for i in range(ITER):
    F = np.array([f(p) for p in pop])
    best.append(-np.max(F))
    G = fitness(F)
    alfa = select(pop, G)
    beta = pop[np.argsort(G)[::-1]]
    childs = np.array([mutation(crossover(a, p)) for a, p in zip(alfa, beta)])
    pop = childs

print(min(best))
plt.plot(best, 'r-')
plt.show()
