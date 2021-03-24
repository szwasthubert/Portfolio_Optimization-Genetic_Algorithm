import listtools
import numpy as np
import pandas as pd
from config import config as cfg, Config
from genetic.operators import OperatorsImpl
from genetic.algorithm import GeneticAlgorithm, AlgorithmParams, AlgorithmResult
from helpers import plotters as plot
from helpers import helper
import matplotlib.pyplot as plt


instruments = ["crypto", "currencies"]
portfolioWeightsDicts = []
RVMatrices = {}
for instrument in instruments:
    for Lambda in np.linspace(0, 1, 2):
        data = pd.read_csv("./data/{0}.csv".format(instrument), parse_dates=True, index_col=0)
        R, V = helper.calculate_RV(data)
        RVMatrices["R_" + instrument] = R
        RVMatrices["V_" + instrument] = V
        chromosome_size = R.shape[0]
        gene_names = data.columns.values

        # przykladowe liczby z kosmosu wziete
        params_crypto = AlgorithmParams(lam=Lambda,#0.67,
                                        R=R,#np.array([1,2,3,4]),
                                        V=V,#np.ones(shape=(4,4)),
                                        chromosome_size=chromosome_size,#4,
                                        gene_names=gene_names)#['BTC', 'ETH', 'LTC', 'XRP'])

        simulation = GeneticAlgorithm(cfg, OperatorsImpl(cfg), params_crypto)
        results = simulation.run()
        solution = results.get_solution()
        portfolioWeightsDicts.append(solution)

print(portfolioWeightsDicts)
print(RVMatrices)
'''
print('Best iteration:', results.best_iteration())
print('Solution:', solution)
print("Algorithm total time: {:.2f}s".format(results.totalTime))


plot.plot_fitness_history(cfg, results)
plot.plot_portfolio_history(cfg, results)
plot.plot_solution(results)
plt.show()
'''
