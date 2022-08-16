from __future__ import annotations
import random


class Individual:
    def __init__(self, name) -> None:
        self.name = name
        self.fitness = random.randint(0, 10)

    def __str__(self) -> str:
        return f'{self.name}: {self.fitness}'

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def create_random_population(cls, num) -> list[Individual]:
        # create a random a, b, ..., j and convert to UPPER, this is my population
        population = []
        for i in range(97, 97 + num):
            population.append(Individual(chr(i).upper()))
        return population
