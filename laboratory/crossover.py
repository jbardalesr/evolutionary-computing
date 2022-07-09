from representation import Individual
import random
from abc import ABC, abstractmethod
import numpy as np
import copy


class Crossover(ABC):
    def __init__(self, probability: float):
        self.probability = probability

    @abstractmethod
    def make(self, p1: Individual, p2: Individual):
        pass


class OnePointCrossover(Crossover):
    def __init__(self, probability: float):
        super().__init__(probability)

    def make(self, p1: Individual, p2: Individual):
        # dos hijos por pareja
        if random.random() < self.probability:
            c1 = copy.deepcopy(p1.getGenotype())
            c2 = copy.deepcopy(p2.getGenotype())
            point = random.randint(1, len(c1) - 2)

            c1[point:], c2[point:] = c2[point:], c1[point:]
            return Individual.newLike(c1, p1), Individual.newLike(c2, p2)
        return None


class NPointCrossover(Crossover):
    def __init__(self, probability: float, n: int):
        super().__init__(probability)
        self.n = n

    def make(self, p1: Individual, p2: Individual):
        # dos hijos por pareja
        if random.random() < self.probability:
            ps = random.sample(range(1, p1.gen_size * p1.n_var - 1), self.n)
            ps.append(0)
            ps.append(p1.gen_size * p1.n_var)
            ps = sorted(ps)
            c1 = copy.deepcopy(p1.getGenotype())
            c2 = copy.deepcopy(p2.getGenotype())
            for i in range(0, self.n + 1):
                if i % 2 == 0:
                    continue
                c1[ps[i]:ps[i + 1]], c2[ps[i]:ps[i + 1]] = c2[ps[i]:ps[i + 1]], c1[ps[i]:ps[i + 1]]

            return Individual.newLike(c1, p1), Individual.newLike(c2, p2)
        return None


class ShuffleCrossover(Crossover):
    def __init__(self, probability: float):
        super().__init__(probability)

    def make(self, p1: Individual, p2: Individual):
        # dos hijos por pareja
        if random.random() < self.probability:
            index = list(range(0, p1.gen_size * p1.n_var))
            random.shuffle(index)

            p1_gen = np.array(p1.getGenotype())
            p2_gen = np.array(p2.getGenotype())

            c1 = np.copy(p1_gen[index])
            c2 = np.copy(p1_gen[index])
            temp = np.copy(p2_gen[index])

            point = random.randint(1, len(c1) - 2)
            # slice swap list isn't equals that slice in numpy
            c1[point:], c2[:point] = temp[point:], temp[:point]

            c1_unshuffle = np.zeros_like(c1, dtype=int)
            c2_unshuffle = np.zeros_like(c2, dtype=int)

            c1_unshuffle[index] = c1[index]
            c2_unshuffle[index] = c2[index]
            return Individual.newLike(c1_unshuffle, p1), Individual.newLike(c2_unshuffle, p2)
        return None


class UniformCrossover(Crossover):
    def __init__(self, probability: float, swap_probability: float):
        super().__init__(probability)
        self.swap_probability = swap_probability

    def make(self, p1: Individual, p2: Individual):
        # dos hijos por pareja
        if random.random() < self.probability:
            # swap a random position i
            c1 = copy.deepcopy(p1.getGenotype())
            c2 = copy.deepcopy(p2.getGenotype())

            for i in range(p1.gen_size * p1.n_var):
                if random.random() < self.swap_probability:
                    c1[i], c2[i] = c2[i], c1[i]
            return Individual.newLike(c1, p1), Individual.newLike(c2, p2)
        return None
