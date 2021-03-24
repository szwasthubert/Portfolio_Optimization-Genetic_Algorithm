#!/usr/bin/env python3

import listtools
import numpy as np
import pandas as pd
from config import config as cfg, Config
from genetic.operators import OperatorsImpl
from genetic.algorithm import GeneticAlgorithm, AlgorithmParams, AlgorithmResult
from helpers import plotters as plot
from helpers import helper
import matplotlib.pyplot as plt
import multiprocessing as mp
import pprint
from datetime import datetime

from typing import List

# Leci pojedynczy przebieg genetycznego
def single_genetic_pass(Lambda: float, R: np.ndarray, V: np.ndarray, chromosome_size: int, gene_names: List[str]):
    params_crypto = AlgorithmParams(lam=Lambda,  # 0.67,
                                    R=R,  # np.array([1,2,3,4]),
                                    V=V,  # np.ones(shape=(4,4)),
                                    chromosome_size=chromosome_size,  # 4,
                                    gene_names=gene_names)  # ['BTC', 'ETH', 'LTC', 'XRP'])

    simulation = GeneticAlgorithm(cfg, OperatorsImpl(cfg), params_crypto)
    results = simulation.run()
    return results.get_solution()


# Po staremu, bez wielowatkowosci
def do_without_threading(instruments: List[str]):
    portfolioWeightsDicts = []
    RVMatrices = {}

    start_time = datetime.timestamp(datetime.now())

    for instrument in instruments:
        data = pd.read_csv("./data/{0}.csv".format(instrument), parse_dates=True, index_col=0)
        R, V = helper.calculate_RV(data)
        RVMatrices["R_" + instrument] = R
        RVMatrices["V_" + instrument] = V
        chromosome_size = R.shape[0]
        gene_names = data.columns.values

        for Lambda in np.linspace(0, 1, 2):
            solution = single_genetic_pass(Lambda, R, V, chromosome_size, gene_names)
            portfolioWeightsDicts.append(solution)

    end_time = datetime.timestamp(datetime.now())
    print('Total computation time: {:.2f}s'.format(end_time - start_time))

    return portfolioWeightsDicts, RVMatrices


# Kazde wywolanie tej funkcji to osobny watek
def single_thread(instrument: str, R: np.ndarray, V: np.ndarray, chromosome_size: int, gene_names: List[str]):
    print('Started thread for instrument:', instrument)
    start_time = datetime.timestamp(datetime.now())
    portfolioWeightsDicts = []
    for Lambda in np.linspace(0, 1, 2):
        solution = single_genetic_pass(Lambda, R, V, chromosome_size, gene_names)
        portfolioWeightsDicts.append(solution)

    #queue.put({instrument: portfolioWeightsDicts})

    end_time = datetime.timestamp(datetime.now())
    elapsed = end_time - start_time
    print('Finished', instrument, '- it took {:.2f}s'.format(elapsed))

    return portfolioWeightsDicts


def do_with_threading(instruments: List[str]):
    portfolioWeightsDicts = []
    RVMatrices = {}

    threadResults = {}
    pool = mp.Pool()
    start_time = datetime.timestamp(datetime.now())
    for instrument in instruments:
        data = pd.read_csv("./data/{0}.csv".format(instrument), parse_dates=True, index_col=0)
        R, V = helper.calculate_RV(data)
        RVMatrices["R_" + instrument] = R
        RVMatrices["V_" + instrument] = V
        chromosome_size = R.shape[0]
        gene_names = data.columns.values

        # argumenty przekazane do funkcji single_thread() musza byc slownikiem
        kw = {'instrument': instrument,
              'R': R.to_numpy(), 'V': V.to_numpy(),
              'chromosome_size': chromosome_size,
              'gene_names': gene_names}

        print('Creating thread for instrument:', instrument)
        threadResults[instrument] = pool.apply_async(single_thread, kwds=kw)

    # Wait for all threads to finish
    pool.close()
    pool.join()
    print('All threads finished')

    for instrument in instruments:
        portfolioWeightsDicts += threadResults[instrument].get()

    end_time = datetime.timestamp(datetime.now())
    print('Total computation time: {:.2f}s'.format(end_time - start_time))

    return portfolioWeightsDicts, RVMatrices


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=2)

    instruments = ["crypto", "currencies"]

    portfolioWeightsDicts, RVMatrices = \
        do_with_threading(instruments) if cfg['threading_enabled'] else do_without_threading(instruments)

    '''
    print('Best iteration:', results.best_iteration())
    print('Solution:', solution)
    print("Algorithm total time: {:.2f}s".format(results.totalTime))
    
    
    plot.plot_fitness_history(cfg, results)
    plot.plot_portfolio_history(cfg, results)
    plot.plot_solution(results)
    plt.show()
    '''


    dict_of_lists = dict()
    for i in range(len(instruments)):
        dict_of_lists[instruments[i]] = portfolioWeightsDicts[i*lambda_counts:(i+1)*lambda_counts]

    list_of_plotter_dicts = []
    for instrument, list_of_returns in dict_of_lists.items():
        list_of_plotter_dicts.append(helper.risk_return_dict_generator(instrument, list_of_returns, RVMatrices["R_" + instrument], RVMatrices["V_" + instrument]))

    plot.efficient_frontier_plotter(list_of_plotter_dicts)
