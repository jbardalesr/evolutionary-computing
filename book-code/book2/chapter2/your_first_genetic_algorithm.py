from __future__ import annotations

import random
import numpy as np
import matplotlib.pyplot as plt


def _util_constraints(g, min, max):
    if max and g > max:
        g = max
    if min and g < min:
        g = min
    return g


def crossover_blend(g1, g2, alpha, min=None, max=None):
    shift = (1.0 + 2.0*alpha)*random.random() - alpha
    new_g1 = (1.0 - shift)*g1 + shift*g2
    new_g2 = shift*g1 + (1.0 - shift)*g2
    return _util_constraints(new_g1, min, max), _util_constraints(new_g2, min, max)


def mutate_gaussian(g, mu, sigma, min=None, max=None):
    mutated_gene = g + random.gauss(mu, sigma)
    return _util_constraints(mutated_gene, min, max)


def select_tournament(population: list[Individual], tournament_size) -> list[Individual]:
    new_offspring = []
    for _ in range(len(population)):
        # select max of each 3 until has len(population) individuals
        candidates = [random.choice(population) for _ in range(tournament_size)]
        new_offspring.append(max(candidates, key=lambda ind: ind.fitness))
    return new_offspring


def func(x):
    return np.sin(x) - 0.2*abs(x)


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
    plt.plot([ind.get_gene() for ind in population], [ind.fitness for ind in population], 'o', color='orange')
    plt.plot(best.get_gene(), best.fitness, 's', color="green")
    plt.title(f"Generation number {generation_number}")
    plt.show()
    plt.close()


class Individual:
    def __init__(self, gene: float) -> None:
        self.gene = gene
        self.fitness = func(self.gene)

    def get_gene(self):
        return self.gene

    @classmethod
    def crossover(cls, parent1: Individual, parent2: Individual):
        child1_gene, child2_gene = crossover_blend(parent1.get_gene(), parent2.get_gene(), 1, -10, 10)
        return Individual(child1_gene), Individual(child2_gene)

    @classmethod
    def mutate(cls, ind: Individual):
        mutated_gene = mutate_gaussian(ind.get_gene(), 0, 1, -10, 10)
        return Individual(mutated_gene)

    @classmethod
    def select(cls, population: list[Individual]):
        return select_tournament(population, tournament_size=3)

    @classmethod
    def create_random(cls):
        return Individual(random.randrange(-1000, 1000)/1000)


# GA CANONICAL FLOW
random.seed(52)
# random.seed(16) # local maximum
POPULATION_SIZE = 10
CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.1
MAX_GENERATION = 10

first_population = [Individual.create_random() for _ in range(POPULATION_SIZE)]
plot_population(first_population, 0)

generation_number = 0

population = first_population.copy()

while generation_number < MAX_GENERATION:
    generation_number += 1

    # SELECTION
    offspring = Individual.select(population)

    # CROSSOVER
    crossed_offspring: list[Individual] = []
    for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CROSSOVER_PROBABILITY:
            kid1, kid2 = Individual.crossover(ind1, ind2)
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
            new_mutant = Individual.mutate(mutant)
            mutated_offspring.append(new_mutant)
        else:
            mutated_offspring.append(mutant)

    population = mutated_offspring.copy()
    plot_population(population, generation_number)
