import random
from datetime import datetime
from typing import List
import numpy as np
import listtools
from config import Config
from genetic.operators import OperatorsBase
from genetic.chromosome import Chromosome


# Current simulation state
class AlgorithmResult:
    def __init__(self):
        self.champion_chromosomes = []
        self.max_values = []
        self.avg_values = []
        self.stds = []
        self.totalTime = 0.0
        self.current_population = None

class AlgorithmParams:
    def __init__(self, lam: float, R: np.ndarray, V: np.ndarray, chromosome_size: int):
        self.lam = lam
        self.R = R
        self.V = V
        self.chromosome_size = chromosome_size


class GeneticAlgorithm:
    def __init__(self, config: Config, operators: OperatorsBase, params: AlgorithmParams):
        self.config = config
        self.operators = operators
        self.params = params
        self.population: List[Chromosome] = []
        self.fitness_values: List[float] = []

    def run(self) -> AlgorithmResult:
        MAX_RUNS = self.config['max_runs']
        result = AlgorithmResult()

        dt_start = datetime.timestamp(datetime.now())

        self.generate_initial_population()

        # symulujemy kolejne iteracje, zapisując wyniki każdej z nich
        for i in range(MAX_RUNS):

            # może już przetwarzać sobie następne, jeśli to nie było ostatnie
            if i < MAX_RUNS - 1:
                self.next_generation()

            std = np.std(self.fitness_values)

            # add the champion chromosome to a list of champions for plotting
            index_of_champion = listtools.max_index_in_list(self.fitness_values)
            result.champion_chromosomes.append(self.population[index_of_champion])

            # add the max/average values to lists for plotting
            result.max_values.append(listtools.max_value_in_list(self.fitness_values))
            result.avg_values.append(listtools.avgList(self.fitness_values))
            result.stds.append(std)

            result.current_population = self.population
            result.iteration = i

        dt_end = datetime.timestamp(datetime.now())
        result.totalTime = dt_end - dt_start

        return result

    def generate_initial_population(self) -> None:
        random.seed()
        self.population = []
        for _ in range(self.config['population_size']):
            self.population.append(Chromosome(
                np.random.rand(self.params.chromosome_size)
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
            parent_indices = self.operators.selection(self.fitness_values)

            # crossover - generate a child based on
            chromosome = self.operators.crossover(self.population[parent_indices[0]], self.population[parent_indices[1]])

            # mutation
            chromosome = self.operators.mutation(chromosome)
            new_population.append(chromosome)

        self.population = new_population
        self.calculate_fitness()

    # Funkcja przystosowania dla pojedynczego chromosomu (osobnika)
    def get_fitness_for_chromosome(self, chromosome_index: int) -> float:
        x = self.population[chromosome_index].portfolio
        # lambda * R' * x - (1 - lambda) * x * v * x'
        return self.params.lam * (self.params.R @ x) - (1 - self.params.lam) * (x @ self.params.V @ np.transpose(x))
