import listtools
import numpy as np
from config import config as cfg, Config
from genetic.operators import OperatorsImpl
from genetic.algorithm import GeneticAlgorithm, AlgorithmParams, AlgorithmResult

import matplotlib.pyplot as plt

# przykladowe liczby z dupy wziete
params_crypto = AlgorithmParams(lam=0.5,
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


def plot_fitness_history(config: Config, result: AlgorithmResult):
    MAX_RUNS = config['max_runs']
    best_index = result.best_iteration()
    plt.figure()
    plt.title("Generation fitness value")
    plt.plot(range(1,MAX_RUNS+1), result.max_values, marker='.', label=r"Best")
    plt.plot(range(1,MAX_RUNS+1), result.avg_values, marker='.', label=r"Average")
    plt.plot([best_index+1], result.max_values[best_index], marker='o', color='r')
    plt.legend(loc='lower right')
    plt.grid()
    plt.xlabel("Generation")
    plt.ylabel("Fitness")


def plot_portfolio_history(config: Config, result: AlgorithmResult):
    MAX_RUNS = config['max_runs']
    plt.figure()
    plt.title("Generation best portfolio distribution")

    for i, name in enumerate(result.gene_names):
        plt.plot(range(1, MAX_RUNS + 1), [x.portfolio[i] for x in result.champion_chromosomes], marker='.', label=name)
        pass

    plt.legend(loc='center right')
    plt.grid()
    plt.xlabel("Generation")
    plt.ylabel("Portfolio distribution")


def plot_solution(result: AlgorithmResult):
    solution = result.get_solution()
    labels = solution.keys()
    sizes = solution.values()

    plt.figure()
    plt.title("Final portfolio distribution")
    plt.pie(sizes, labels=labels, autopct='%1.1f%%',
            startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


plot_fitness_history(cfg, results)
plot_portfolio_history(cfg, results)
plot_solution(results)
plt.show()
