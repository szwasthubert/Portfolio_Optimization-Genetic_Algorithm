#!/usr/bin/env python3

import listtools
import numpy as np
from config import config as cfg, Config
from genetic.operators import OperatorsImpl
from genetic.algorithm import GeneticAlgorithm, AlgorithmParams, AlgorithmResult
from helpers import plotters as plot
import matplotlib.pyplot as plt

# przykladowe liczby z kosmosu wziete
params_crypto = AlgorithmParams(lam=0.67,
                                R=np.array([1,2,3,4]),
                                V=np.ones(shape=(4,4)),
                                chromosome_size=4,
                                gene_names=['BTC', 'ETH', 'LTC', 'XRP'])

simulation = GeneticAlgorithm(cfg, OperatorsImpl(cfg), params_crypto)
results = simulation.run()
solution = results.get_solution()

print('Best iteration:', results.best_iteration())
print('Solution:', solution)
print("Algorithm total time: {:.2f}s".format(results.totalTime))


plot.plot_fitness_history(cfg, results)
plot.plot_portfolio_history(cfg, results)
plot.plot_solution(results)
plt.show()
