#!/usr/bin/env python3
from typing import List

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

    return portfolioWeightsDicts, RVMatrices


# Kazde wywolanie tej funkcji to osobny watek
def single_thread(instrument: str, queue: mp.Queue, R: np.ndarray, V: np.ndarray, chromosome_size: int, gene_names: List[str]):
    portfolioWeightsDicts = []
    for Lambda in np.linspace(0, 1, 2):
        solution = single_genetic_pass(Lambda, R, V, chromosome_size, gene_names)
        portfolioWeightsDicts.append(solution)

    queue.put({instrument: portfolioWeightsDicts})


def do_with_threading(instruments: List[str]):
    portfolioWeightsDicts = []
    RVMatrices = {}

    threads = []
    queue = mp.Queue()
    for instrument in instruments:
        data = pd.read_csv("./data/{0}.csv".format(instrument), parse_dates=True, index_col=0)
        R, V = helper.calculate_RV(data)
        RVMatrices["R_" + instrument] = R
        RVMatrices["V_" + instrument] = V
        chromosome_size = R.shape[0]
        gene_names = data.columns.values

        # argumenty przekazane do funkcji single_thread() musza byc slownikiem
        kw = {'instrument': instrument,
              'queue': queue,
              'R': R, 'V': V,
              'chromosome_size': chromosome_size,
              'gene_names': gene_names}

        print('Starting thread for instrument:', instrument)
        th = mp.Process(target=single_thread, kwargs=kw, name=instrument)
        th.start()
        threads.append(th)

    for th in threads:
        print('Finished thread', th)
        th.join()

    # Magic here
    instrument_dicts = [queue.get() for _ in threads]
    instrument_dicts = {k: v for d in instrument_dicts for k, v in d.items()}

    for instrument in instruments:
        portfolioWeightsDicts += instrument_dicts[instrument]

    return portfolioWeightsDicts, RVMatrices


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=2)

    instruments = ["crypto", "currencies"]

    portfolioWeightsDicts, RVMatrices = \
        do_with_threading(instruments) if cfg['threading_enabled'] else do_without_threading(instruments)

    print('\nportfolioWeightsDicts')
    pp.pprint(portfolioWeightsDicts)
    print('\nRVMatrices')
    pp.pprint(RVMatrices)

    '''
    print('Best iteration:', results.best_iteration())
    print('Solution:', solution)
    print("Algorithm total time: {:.2f}s".format(results.totalTime))
    
    
    plot.plot_fitness_history(cfg, results)
    plot.plot_portfolio_history(cfg, results)
    plot.plot_solution(results)
    plt.show()
    '''
