from abc import ABC, abstractmethod

import random
import numpy as np
from typing import List

import listtools
from config import Config
from genetic.chromosome import Chromosome


class OperatorsBase(ABC):
    def __init__(self, *args):
        super().__init__(*args)

    @abstractmethod
    def mutation(self, chromosome: Chromosome) -> Chromosome:
        raise NotImplementedError('Mutation is not implemented!')

    @abstractmethod
    def crossover(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        raise NotImplementedError('Crossover is not implemented!')

    # Selekcja
    @abstractmethod
    def selection(self, fitness_values: List[float]) -> List[int]:
        raise NotImplementedError('Selection is not implemented!')


class OperatorsImpl(OperatorsBase):
    def __init__(self, config: Config, *args):
        super().__init__(*args)
        self.config = config

    # Mutation
    def mutation(self, chromosome: Chromosome) -> Chromosome:
        random.seed()

        if random.random() > self.config['mutation_probability']:
            return chromosome

        new_gens = []
        for gen in chromosome.portfolio:
            if random.random() <= self.config['mutation_gen_probability']:
                mut_val = self.config['mutation_coefficient']
                coeff = random.random() * mut_val - mut_val / 2
                new_gens += [max(0.0, gen + coeff)]
            else:
                new_gens += [gen]

        return Chromosome(np.array(new_gens))

    # Crossover
    def crossover(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        random.seed()

        if random.random() > self.config['crossover_rate']:
            if random.random() < 0.5:
                return parent1
            return parent2
        else:
            # random combination crossover
            mask = np.random.choice(a=[False, True], size=len(parent1.portfolio), p=[.5, .5])
            child = []
            for i, entry in enumerate(mask):
                child += [parent1.portfolio[i] if entry else parent2.portfolio[i]]

            return Chromosome(np.array(child))

    # Selekcja metodą koła ruletki
    def selection(self, fitness_values: List[float]) -> List[int]:

        probabilities = listtools.normListSumTo(fitness_values, 1)
        parent_indices = []
        random.seed()
        parent1_probability = random.random()
        parent2_probability = random.random()

        summ = 0
        for i in range(self.config['population_size']):
            if len(parent_indices) == 2:
                break
            next_sum = summ + probabilities[i]
            if next_sum >= parent1_probability >= summ:
                parent_indices.append(i)
            if next_sum >= parent2_probability >= summ:
                parent_indices.append(i)
            summ = next_sum
        return parent_indices

