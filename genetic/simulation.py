import multiprocessing

import random
from typing import List

from config import Config
from genetic.algorithm import AlgorithmBase
from genetic.chromosome import Chromosome


class Simulation:
    def __init__(self, config: Config, algorithm: AlgorithmBase):
        self.config = config
        self.algorithm = algorithm
        self.population: List[Chromosome] = []
        self.fitness_values: List[float] = []

    def generate_initial_population(self) -> None:
        random.seed()
        self.population = []
        for _ in range(self.config['population_size']):
            self.population.append(Chromosome(
                random.random() * self.config['max_gain_value'],
                random.random() * self.config['max_integral_value'],
                random.random() * self.config['max_derivative_value']
            ))

        self.calculate_fitness()

    def calculate_fitness(self) -> None:
        self.fitness_values = []
        for chromosomeIndex in range(self.config['population_size']):
            self.fitness_values.append(self.get_fitness_for_chromosome(chromosomeIndex))

    def next_generation(self) -> None:
        # wyznacz przystosowanie dla pokolenia
        # wyselekcjonuj rodzicow
        # krzyzuj ich
        # ewentualne mutacje
        new_population = []

        # generate a new population based on fitness values
        for chromosomeIndex in range(self.config['population_size']):
            # selection - find two parents of new chromosome
            parent_indices = self.algorithm.selection(self.fitness_values)

            # crossover - generate a child based on
            chromosome = self.algorithm.crossover(self.population[parent_indices[0]], self.population[parent_indices[1]])

            # mutation
            chromosome = self.algorithm.mutation(chromosome)
            new_population.append(chromosome)

        self.population = new_population
        self.calculate_fitness()

    def get_fitness_for_chromosome(self, chromosome_index: int) -> float:
        chromosome = self.population[chromosome_index]
        f = (chromosome.x1 - 0.5) ** 2 + (chromosome.x2 - 0.5) ** 2 + (chromosome.x3 - 0.5) ** 2
        return 1 - f

    def get_fitness_for_chunk(self, fits: multiprocessing.Array, chunk: List[int]):
        for idx in chunk:
            fits[idx] = self.get_fitness_for_chromosome(idx)