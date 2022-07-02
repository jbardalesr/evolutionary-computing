from __future__ import annotations
import random
import statistics
import time
import sys
from typing import Callable


def _generate_parent(length: int, geneSet: list, gen_fitness: Callable[[float], float]) -> Chromosome:
    genes = []
    while len(genes) < length:
        sampleSize = min(length - len(genes), len(geneSet))
        genes.extend(random.sample(geneSet, sampleSize))
    fitness = gen_fitness(genes)
    return Chromosome(genes, fitness)


def _mutate(parent: Chromosome, geneSet: list, get_fitness: Callable):
    childGenes = parent.Genes[:]
    index = random.randrange(0, len(parent.Genes))
    newGene, alternate = random.sample(geneSet, 2)
    childGenes[index] = alternate if newGene == childGenes[index] else newGene
    fitness = get_fitness(childGenes)
    return Chromosome(childGenes, fitness)


def get_best(get_fitness: Callable, targetLen: int, optimalFitness: float, geneSet: list, display: Callable):
    random.seed()

    def fnMutate(parent: Chromosome):
        return _mutate(parent, geneSet, get_fitness)

    def fnGeneratePath():
        return _generate_parent(targetLen, geneSet, get_fitness)

    for improvement in _get_improvement(fnMutate, fnGeneratePath):
        display(improvement)
        if not optimalFitness > improvement.Fitness:
            return improvement


def _get_improvement(new_child: Callable[[Chromosome], Chromosome], generate_parent: Callable[[], Chromosome]) -> list[Chromosome]:
    bestParent = generate_parent()
    yield bestParent
    while True:
        child = new_child(bestParent)
        if bestParent.Fitness > child.Fitness:
            continue
        if not child.Fitness > bestParent.Fitness:
            bestParent = child
            continue
        yield child
        bestParent = child


class Chromosome:
    Genes = None
    Fitness = None

    def __init__(self, genes, fitness: float) -> None:
        self.Genes = genes
        self.Fitness = fitness


class Benchmark:
    @staticmethod
    def run(function):
        timings = []
        stdout = sys.stdout
        for i in range(100):
            sys.stdout = None
            startTime = time.time()
            function()
            seconds = time.time() - startTime
            sys.stdout = stdout
            timings.append(seconds)
            mean = statistics.mean(timings)
            if i < 10 or i % 10 == 9:
                print("{0} {1:3.2f} {2:3.2f}".format(1 + i, mean, statistics.stdev(timings, mean) if i > 1 else 0))
