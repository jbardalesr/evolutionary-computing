# import part
import random
import pandas as pd
import matplotlib.pyplot as plt
from chapter3.individual import Individual

# tournament selection
POPULATION_SIZE = 10
TOURNAMENT_SIZE = 3

# generate a population with 10 individuals
population = Individual.create_random_population(POPULATION_SIZE)

# select randomly 3 individuals
candidates = [random.choice(population) for _ in range(TOURNAMENT_SIZE)]

# max of the previous selected
best = [max(candidates, key=lambda ind: ind.fitness)]


def plot_individuals(individual_set: list[Individual]):
    # visualization
    df = pd.DataFrame({'name': [ind.name for ind in individual_set],
                       'fitness': [ind.fitness for ind in individual_set]
                       })
    df.plot.bar(x='name', y='fitness', rot=0)
    plt.show()


plot_individuals(population)
plot_individuals(candidates)
plot_individuals(best)
