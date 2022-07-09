from representation import Individual
import random
from abc import ABC, abstractmethod
import copy


class Mutation(ABC):
    def __init__(self, probability: float):
        self.probability = probability

    @abstractmethod
    def make(self, p1: Individual, p2: Individual):
        pass


class OneFlipMutation(Mutation):
    def __init__(self, probability: float):
        super().__init__(probability)

    def make(self, ind: Individual):
        mut = copy.deepcopy(ind.getGenotype())
        if random.random() < self.probability:
            # punto aleatorio de la cadena
            point = random.randint(0, len(mut) - 1)

            if len(mut) > ind.n_var:
                mut[point] = (mut[point] + 1) % 2
            else:
                mut[point] = random.uniform(ind.domain[0], ind.domain[1])
            return Individual.newLike(mut, ind)
        return None


class UniformMutation(Mutation):
    def __init__(self, probability: float):
        super().__init__(probability)

    def make(self, ind: Individual):
        mut = copy.deepcopy(ind.getGenotype())
        if random.random() < self.probability:
            # punto aleatorio de la cadena
            p = 0.5
            for i in range(len(mut)):
                if random.random() < p:
                    mut[i] = (mut[i] + 1) % 2
            return Individual.newLike(mut, ind)
        return None


class SwapMutation(Mutation):
    def __init__(self, probability: float):
        super().__init__(probability)

    def make(self, ind: Individual):
        mut = copy.deepcopy(ind.getGenotype())
        if random.random() < self.probability:
            i, j = random.sample(range(len(mut)), k=2)
            mut[i], mut[j] = mut[j], mut[i]
            return Individual.newLike(mut, ind)
        return None


class ReversingMutation(Mutation):
    def __init__(self, probability: float):
        super().__init__(probability)

    def make(self, ind: Individual):
        mut = copy.deepcopy(ind.getGenotype())
        if random.random() < self.probability:
            point = random.randint(0, len(mut) - 2)
            mut[point] = (mut[point + 1] + 1) % 2
            return Individual.newLike(mut, ind)
        return None
