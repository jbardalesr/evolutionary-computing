from __future__ import annotations
from bin_repr import dec2bin, bin2gray, my_map, inverse_map, bin2dec, gray2bin
import random
from typing import NamedTuple


class IndividualArguments(NamedTuple):
    domain: tuple[int, int]
    eps: float
    n_var: int
    gen_size: int


class Individual():
    def __init__(self, phenotype: list[float], args: IndividualArguments):
        self.domain = args.domain
        self.eps = args.eps
        self.n_var = args.n_var
        self.gen_size = args.gen_size
        self.phenotype = phenotype

    def getGenotype(self):
        list_repr: list[int] = []
        for gen in self.phenotype:
            list_repr.extend(bin2gray(dec2bin(num=my_map(gen, self.domain[0], self.domain[1], self.eps), bits=self.gen_size)))
        return list_repr

    @classmethod
    def new(cls, genotype, args: IndividualArguments):
        phenotype: list[int] = []
        for k in range(args.n_var):
            gen = genotype[args.gen_size * k:args.gen_size * (k + 1)]
            phenotype.append(inverse_map(bin2dec(gray2bin(gen)), args.domain[0], args.eps))
        return cls(phenotype, args)

    @staticmethod
    def newLike(genotype: list[int], parent: Individual):
        args = IndividualArguments(parent.domain, parent.eps, parent.n_var, parent.gen_size)
        return Individual.new(genotype, args)

    @classmethod
    def newRandom(cls, args: IndividualArguments):
        phenotype = [round(random.uniform(args.domain[0], args.domain[1]), 6) for _ in range(args.n_var)]
        return cls(phenotype, args)
