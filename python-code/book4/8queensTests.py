from __future__ import annotations
import unittest
import datetime
import genetic


def get_fitness(genes, size):
    board = Board(genes, size)
    rowsWithQueens = set()
    colsWithQueens = set()
    northEastDiagonalWithQueens = set()
    southEastDiagonalWithQueens = set()
    for row in range(size):
        for col in range(size):
            if board.get(row, col) == 'Q':
                rowsWithQueens.add(row)
                colsWithQueens.add(col)
                northEastDiagonalWithQueens.add(row + col)
                southEastDiagonalWithQueens.add(size - 1 - row + col)
    total = 4 * size - len(rowsWithQueens) - len(colsWithQueens) - len(northEastDiagonalWithQueens) - len(southEastDiagonalWithQueens)
    return Fitness(total)


def display(candidate: genetic.Chromosome, startTime, size):
    timeDiff = datetime.datetime.now() - startTime
    board = Board(candidate.Genes, size)
    board.print()
    print("{0}\t- {1}\t{2}".format(' '.join(map(str, candidate.Genes)), candidate.Fitness, str(timeDiff)))


class EightQueenTest(unittest.TestCase):
    def test(self, size=8):
        geneset = [i for i in range(size)]
        startTime = datetime.datetime.now()

        def fnDisplay(candidate):
            display(candidate, startTime, size)

        def fnGetFitness(genes):
            return get_fitness(genes, size)

        optimalFitness = Fitness(0)
        best = genetic.get_best(fnGetFitness, 2 * size, optimalFitness, geneset, fnDisplay)
        self.assertTrue(not optimalFitness > best.Fitness)

    def test_benchmark(self):
        genetic.Benchmark.run(lambda: self.test(20))


class Board:
    def __init__(self, genes, size) -> None:
        board = [['.'] * size for _ in range(size)]
        for index in range(0, len(genes), 2):
            row = genes[index]
            column = genes[index + 1]
            board[column][row] = 'Q'
        self._board = board

    def get(self, row, column):
        return self._board[column][row]

    def print(self):
        for i in reversed(range(len(self._board))):
            print(' '.join(self._board[i]))


class Fitness:
    Total = None

    def __init__(self, total) -> None:
        self.Total = total

    def __gt__(self, other: Fitness):
        return self.Total < other.Total

    def __str__(self) -> str:
        return "{0}".format(self.Total)
