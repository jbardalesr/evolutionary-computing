import random
from chapter3.individual import Individual

# Elite selection: this method is based on rank selection but the difference is that the best individual is selected


def selection_rank_with_elite(individuals: list[Individual], elite_size=0):
    sorted_individuals = sorted(
        individuals, key=lambda ind: ind.fitness, reverse=True)
    rank_distance = 1/len(individuals)
    ranks = [1 - i*rank_distance for i in range(len(individuals))]
    ranks_sum = sum(ranks)
    # we select those with the highest fitness
    selected = sorted_individuals[0:elite_size]

    #  we run through all except what we select
    for i in range(len(sorted_individuals) - elite_size):
        shave = random.random() * ranks_sum
        rank_sum = 0
        for i in range(len(sorted_individuals)):
            rank_sum += ranks[i]
            if rank_sum > shave:
                selected.append(sorted_individuals[i])
                break

    return selected


POPULATION_SIZE = 5
random.seed(3)

population = Individual.create_random_population(POPULATION_SIZE)
selected = selection_rank_with_elite(population, elite_size=2)

print(f'Population: {population}')
print(f'Selected: {selected}')
