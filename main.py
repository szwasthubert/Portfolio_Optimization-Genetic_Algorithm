print("Minimalizuje funkcje: f(x1,x2,x3) = (x1-0.5)^2 + (x2-0.5)^2 + (x3-0.5)^2")

import numpy as np
from datetime import datetime

import listtools
from config import config as cfg
from genetic.algorithm import GeneticAlgorithmImpl
from genetic.simulation import Simulation


simulation = Simulation(cfg, GeneticAlgorithmImpl(cfg))

# Current simulation state
class SimulationStatus():
    def __init__(self):
        self.champion_chromosomes = []
        self.max_values = []
        self.avg_values = []
        self.stds = []
        self.totalTime = 0.0
        self.current_population = None
        self.running = False
        self.drawEvent = False
        self.kill = False


# Ta funkcja wywołuje się w osobnym watku (w tle) żeby nie blokować GUI
def run_sim():
    MAX_RUNS = cfg['max_runs']
    status = SimulationStatus()
    status.running = True

    dt_start = datetime.timestamp(datetime.now())

    simulation.generate_initial_population()

    # symulujemy kolejne iteracje, zapisując wyniki każdej z nich
    for i in range(MAX_RUNS):

        # populacja i fitness z aktualnego pokolenia
        population = simulation.population
        fitness_values = simulation.fitness_values

        # może już przetwarzać sobie następne, jeśli to nie było ostatnie
        if i < MAX_RUNS - 1:
            simulation.next_generation()

        std = np.std(fitness_values)

        # add the champion chromosome to a list of champions for plotting
        index_of_champion = listtools.max_index_in_list(fitness_values)
        status.champion_chromosomes.append(population[index_of_champion])

        # add the max/average values to lists for plotting
        status.max_values.append(listtools.max_value_in_list(fitness_values))
        status.avg_values.append(listtools.avgList(fitness_values))
        status.stds.append(std)

        status.current_population = population
        status.iteration = i

        if status.kill is True:
            # status.running = False
            return

    dt_end = datetime.timestamp(datetime.now())
    status.totalTime = dt_end - dt_start

    status.running = False
    return status


status = run_sim()

best_index = listtools.max_index_in_list(status.max_values)
best_chromosome = status.champion_chromosomes[best_index]

print('Best iteration:', best_index)
print(best_chromosome)

