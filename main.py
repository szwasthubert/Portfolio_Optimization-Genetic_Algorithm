print("Minimalizuje funkcje: f(x1,x2,x3) = (x1-0.2)^2 + (x2-0.8)^2 + (x3-0.5)^2")

import numpy as np
from datetime import datetime

import listtools
from config import config as cfg
from genetic.operators import OperatorsImpl
from genetic.algorithm import GeneticAlgorithm, AlgorithmParams

params_crypto = AlgorithmParams(1,2,3,4)

simulation = GeneticAlgorithm(cfg, OperatorsImpl(cfg), params_crypto)
results = simulation.run()

best_index = listtools.max_index_in_list(results.max_values)
best_chromosome = results.champion_chromosomes[best_index]

print('Best iteration:', best_index)
print(best_chromosome)
print("Algorithm total time: {:.2f}s".format(results.totalTime))

