# import part
from inspect import stack
import random
from shutil import which
from turtle import color
import pandas as pd
import matplotlib.pyplot as plt
from soupsieve import select
from chapter3.individual import Individual

# https://drive.google.com/drive/folders/1PVvPqO5JbI8gRTffDCD61O2v9BH-Y-JZ

# proportional selection
random.seed(4)
POPULATION_SIZE = 5

unsorted_population = Individual.create_random_population(POPULATION_SIZE)
population = sorted(unsorted_population,
                    key=lambda ind: ind.fitness, reverse=True)

fitness_sum = sum([ind.fitness for ind in population])
fitness_map = {}
for i in population:
    # the one with the highest fitness has a high probability of being selected.
    i_prob = round(100 * i.fitness/fitness_sum)
    i_label = f'{i.name} | fitness: {i.fitness}, prob: {i_prob}%'
    fitness_map[i_label] = i.fitness

# visualization
index = ["Sectors"]

df = pd.DataFrame(fitness_map, index=index)
df.plot.barh(stacked=True)
for _ in range(POPULATION_SIZE):
    # scale vertical line to all sectors
    plt.axvline(x=random.random()*fitness_sum, linewidth=5, color="black")
    plt.tick_params(axis='x', which='both', bottom=False,
                    top=False, labelbottom=False)
plt.title("Proportional selection")
plt.show()


def selection_proportional(individuals: list[Individual]) -> list[Individual]:
    sorted_individuals = sorted(
        individuals, key=lambda ind: ind.fitness, reverse=True)
    fitness_sum = sum([ind.fitness for ind in individuals])
    selected: list[Individual] = []

    for _ in range(len(sorted_individuals)):
        # giramos la ruleta tantos individuos tenga
        shave = random.random() * fitness_sum
        roulette_sum = 0
        # recorremos los individuos en orden decreciente
        for ind in sorted_individuals:
            # como se recorre en orden decreciente tenemos que sumar el valor del fitness para saber donde cae
            roulette_sum += ind.fitness
            # en el primero que sea mayor es cuando cae la ruleta asi que lo seleccionamos
            if roulette_sum > shave:
                selected.append(ind)
                #
                break
    return selected


selected = selection_proportional(population)
print(f'Population: {population}')
print(f'Selected: {selected}')
