import listtools
import numpy as np
from config import config as cfg
from genetic.operators import OperatorsImpl
from genetic.algorithm import GeneticAlgorithm, AlgorithmParams

# przykladowe liczby z dupy wziete
params_crypto = AlgorithmParams(lam=0.5,
                                R=np.array([1,2,3,4]),
                                V=np.ones(shape=(4,4)),
                                chromosome_size=4,
                                gene_names=['BTC', 'ETH', 'LTC', 'XRP'])

simulation = GeneticAlgorithm(cfg, OperatorsImpl(cfg), params_crypto)
results = simulation.run()
solution = results.get_solution()

# W ogóle w zmiennej results są rzeczy
# które można wyprintować za pomocą matplotliba (np historia funkcji fitness kazdej iteracji)
# Przykład użycia jest w moim projekcie na MMWD (app.py czy jakoś tak, klasa cośtam z Results w nazwie)

print('Best iteration:', results.best_iteration())
print(solution)
print("Algorithm total time: {:.2f}s".format(results.totalTime))

