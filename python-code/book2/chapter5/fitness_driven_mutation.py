# We run several mutations and pick the best one, if all mutations are worse than the original individual, then we leave the original without mutation
import copy
import random
from math import sin


def func(x):
    return sin(x) - 2*abs(x)


class Individual:
    def __init__(self, gene_list: list[float]) -> None:
        self.gene_list = gene_list
        self.fitness = func(self.gene_list[0])

    def __str__(self) -> str:
        return f'x: {self.gene_list[0]}, fitness: {self.fitness}'

def mutation_fitness_driven_random_deviation(ind: Individual, mu, sigma, p, max_tries=3):
    for t in range(0, max_tries):
        mut_genes = copy.deepcopy(ind.gene_list) # a single element in an array
        for i in range(len(mut_genes)):
            if random.random() < p:
                mut_genes[i] += random.gauss(mu, sigma)
        mut = Individual(mut_genes)
        # one by one select the individual with highest fitness
        if ind.fitness < mut.fitness:
            return mut
    # else return ind without mutation
    return ind

ind = Individual([random.uniform(-10, 10)])
mut = mutation_fitness_driven_random_deviation(ind, 0, 1, 3)

print(f'Original: ({ind})')
print(f'Mutated: ({mut})')