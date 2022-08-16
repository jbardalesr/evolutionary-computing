import random
import pandas as pd
import matplotlib.pyplot as plt
from individual import Individual

POPULATION_SIZE = 5
random.seed(18)

unsorted_population = Individual.create_random_population(POPULATION_SIZE)
population = sorted(unsorted_population,
                    key=lambda ind: ind.fitness, reverse=True)

fitness_sum = sum([ind.fitness for ind in population])
fitness_map = {}
for i in population:
    # for each individual its fitness is the probability to be selected.
    i_prob = round(100 * i.fitness/fitness_sum)
    i_label = f'{i.name} | fitness: {i.fitness}, prob: {i_prob}%'
    fitness_map[i_label] = i.fitness

proportional_df = pd.DataFrame(fitness_map, index=["Sectors"])
proportional_df.plot.barh(stacked=True)
plt.tick_params(axis='x', which='both', bottom=False,
                top=False, labelbottom=False)
plt.title("Fitness Proportional Sectors")
plt.show()

rank_step = 1/POPULATION_SIZE
rank_sum = sum([1 - rank_step*i for i in range(POPULATION_SIZE)])
rank_map = {}

for i in range(POPULATION_SIZE):
    i_rank = i + 1
    i_rank_proportion = 1 - i*rank_step
    i_prob = round(100*i_rank_proportion/rank_sum)
    i_label = f'{population[i].name} | rank: {i_rank}, prob: {i_prob}%'
    rank_map[i_label] = i_rank_proportion

# VISUALIZATION
rank_df = pd.DataFrame(rank_map, index=["Sectors"])
rank_df.plot.barh(stacked=True)
plt.tick_params(axis='x', which='both', bottom=False,
                top=False, labelbottom=False)
plt.title("Rank Proportional Sectors")
plt.show()


def selection_rank(individuals: list[Individual]):
    sorted_individuals = sorted(
        individuals, key=lambda ind: ind.fitness, reverse=True)
    rank_distance = 1/len(individuals)
    ranks = [1 - i*rank_distance for i in range(len(individuals))]
    ranks_sum = sum(ranks)

    selected: list[Individual] = []
    
    for _ in range(len(sorted_individuals)):
        shave = random.random()*ranks_sum
        rank_sum = 0
        for i in range(len(sorted_individuals)):
            rank_sum += ranks[i]
            if rank_sum > shave:
                selected.append(sorted_individuals[i])
                break
    return selected


selected = selection_rank(unsorted_population)

print(f"Population: {population}")
print(f"Selected: {selected}")
