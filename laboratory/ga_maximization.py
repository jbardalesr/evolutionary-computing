from __future__ import annotations
import copy

import math
import random

from matplotlib import pyplot as plt
import bin_repr as bi
import numpy as np

a = -10
b = 10
epsilon = 6.1038e-4
N = round((b - a) / epsilon) + 1
bits = math.floor(math.log2(N)) + 1  # = ceil

func = lambda x: np.sin(x) - 0.2 * abs(x)


class Individual:
    def __init__(self, value: float) -> None:
        self.value = value
        self.fitness = func(value)

    @classmethod
    def new(cls, genotype: list[int]):
        value = bi.bin2dec(bi.gray2bin(genotype))
        return cls(bi.inverse_map(value, a, epsilon))

    def getGenotype(self):
        shift = bi.my_map(self.value, a, b, epsilon)
        return bi.bin2gray(bi.dec2bin(shift, bits))


def crossover(p1: Individual, p2: Individual) -> list[Individual]:
    # one-point crossover
    point = random.randint(1, bits - 2)
    c1, c2 = copy.deepcopy(p1.getGenotype()), copy.deepcopy(p2.getGenotype())
    c1[point:], c2[point:] = c2[point:], c1[point:]

    return Individual.new(c1), Individual.new(c2)


def mutate(ind: Individual):
    # bit-flip mutation
    mut = copy.deepcopy(ind.getGenotype())
    point = random.randint(0, bits - 1)
    g1 = mut[point]
    mut[point] = (g1 + 1) % 2
    return Individual.new(mut)


def select(population: list[Individual]):
    tournament_size = 3
    new_offspring = []
    for _ in range(len(population)):
        candidates = [random.choice(population) for _ in range(tournament_size)]
        new_offspring.append(max(candidates, key=lambda ind: ind.fitness))
    return new_offspring


def create_random():
    return Individual(random.random() * (b - a) + a)


def get_best(population: list[Individual]) -> Individual:
    best = population[0]
    for ind in population:
        if ind.fitness > best.fitness:
            best = ind
    return best


def plot_population(population: list[Individual], generation_number: int):
    best = get_best(population)
    x = np.linspace(-10, 10)

    plt.plot(x, func(x), '--', color="blue")
    plt.plot([ind.value for ind in population],
             [ind.fitness for ind in population], 'o', color='orange')
    plt.plot(best.value, best.fitness, 's', color="green")
    plt.title(f"Generation number {generation_number}")
    plt.show()
    plt.close()


# GA CANONICAL FLOW
random.seed(52)
# random.seed(16) # local maximum
POPULATION_SIZE = 10
CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.5
MAX_GENERATION = 15


first_population: list[Individual] = [create_random() for _ in range(POPULATION_SIZE)]

generation_number = 0

population = first_population.copy()

while generation_number < MAX_GENERATION:
    generation_number += 1

    # SELECTION
    offspring = select(population)

    # CROSSOVER
    crossed_offspring: list[Individual] = []
    for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CROSSOVER_PROBABILITY:
            kid1, kid2 = crossover(ind1, ind2)
            crossed_offspring.append(kid1)
            crossed_offspring.append(kid2)
        else:
            crossed_offspring.append(ind1)
            crossed_offspring.append(ind2)

    # MUTATION
    mutated_offspring: list[Individual] = []
    # we mutate each offspring
    for mutant in crossed_offspring:
        if random.random() < MUTATION_PROBABILITY:
            new_mutant = mutate(mutant)
            mutated_offspring.append(new_mutant)
        else:
            mutated_offspring.append(mutant)

    population = mutated_offspring.copy()
    plot_population(population, generation_number)
