from abc import ABC, abstractmethod

import random
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
        max_P_value = self.config['max_gain_value']
        max_I_value = self.config['max_integral_value']
        max_D_value = self.config['max_derivative_value']

        if random.random() < self.config['mutation_probability'] / 3:
            if random.random() < 1/2:
                chromosome.x1 = chromosome.x1 + random.random() / 10.0 * max_P_value
            else:
                chromosome.x1 = chromosome.x1 - random.random() / 10.0 * max_P_value
        if chromosome.x1 < 0 or chromosome.x1 > max_P_value:
            chromosome.x1 = random.random() * max_P_value

        elif random.random() < self.config['mutation_probability'] * 2 / 3:
            if random.random() < 1 / 2:
                chromosome.x2 = chromosome.x2 + random.random() / 10.0 * max_I_value
            else:
                chromosome.x2 = chromosome.x2 - random.random() / 10.0 * max_I_value
        if chromosome.x2 < 0 or chromosome.x2 > max_I_value:
            chromosome.x2 = random.random() * max_I_value

        elif random.random() < self.config['mutation_probability']:
            if random.random() < 1 / 2:
                chromosome.x3 = chromosome.x3 + random.random() / 10.0 * max_D_value
            else:
                chromosome.x3 = chromosome.x3 - random.random() / 10.0 * max_D_value
        if chromosome.x3 < 0 or chromosome.x3 > max_D_value:
            chromosome.x3 = random.random() * max_D_value

        return chromosome

    # Crossover
    def crossover(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        random.seed()

        if random.random() > self.config['crossover_rate']:
            return parent1
        else:
            # random combination crossover
            number = random.random()
            if number < 1.0 / 6:
                return Chromosome(parent1.x1, parent2.x2, parent2.x3)
            elif number < 2.0 / 6:
                return Chromosome(parent2.x1, parent1.x2, parent1.x3)
            elif number < 3.0 / 6:
                return Chromosome(parent1.x1, parent2.x2, parent1.x3)
            elif number < 4.0 / 6:
                return Chromosome(parent1.x1, parent1.x2, parent2.x3)
            elif number < 5.0 / 6:
                return Chromosome(parent2.x1, parent1.x2, parent2.x3)
            else:
                return Chromosome(parent2.x1, parent2.x2, parent2.x3)

    # Selection
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

