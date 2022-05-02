# IMPORT PART
from pickle import POP
import random
import pandas as pd
import matplotlib.pyplot as plt
from scipy import rand
from soupsieve import select
from chapter3.individual import Individual

# Universal stochastic sampling: this method is similar to proportional selection with the difference that the roulette is divided into N equally spaced cut-off points.
# This ensure that the individuals are selected according to the following principle - many good individuals, same average individuals and few bad individuals
# SELECTION
POPULATION_SIZE = 5
random.seed(9)

unsorted_population = Individual.create_random_population(POPULATION_SIZE)
population = sorted(unsorted_population,
                    key=lambda ind: ind.fitness, reverse=True)

fitness_sum = sum([ind.fitness for ind in population])
fitness_map = {}
for i in population:
    i_prob = round(100*i.fitness/fitness_sum)
    i_label = f'{i.name} | fitness: {i.fitness}, prob: {i_prob}%'
    fitness_map[i_label] = i.fitness

# VISUALIZATION
index = ['Sectors']
df = pd.DataFrame(fitness_map, index=index)
df.plot.barh(stacked=True)
# like a pizza each individuals has a piece same
distance = fitness_sum/POPULATION_SIZE

# initial shift is random thereafter the shift are the same
shift = random.random() * distance
for i in range(POPULATION_SIZE):
    plt.axvline(x=shift + distance*i, linewidth=5, color='black')
    plt.tick_params(axis='x', which='both', bottom=False,
                    top=False, labelbottom=False)

plt.show()


def selection_stochastic_universal_sampling(individuals: list[Individual]):
    sorted_individuals = sorted(
        individuals, key=lambda ind: ind.fitness, reverse=True)
    fitness_sum = sum([ind.fitness for ind in individuals])

    distance = fitness_sum/len(individuals)
    shift = random.uniform(0, distance)
    borders = [shift + i*distance for i in range(len(individuals))]

    selected: list[individuals] = []
    # selected as many borders as I have
    for border in borders:
        i = 0
        roulette_sum = sorted_individuals[i].fitness

        # sum until you have an individual fall on the border
        while roulette_sum < border:
            i += 1
            roulette_sum += sorted_individuals[i].fitness
        # select the individual
        selected.append(sorted_individuals[i])

    return selected


selected = selection_stochastic_universal_sampling(unsorted_population)
print(f'Population: {population}')
print(f'Selected: {selected}')
