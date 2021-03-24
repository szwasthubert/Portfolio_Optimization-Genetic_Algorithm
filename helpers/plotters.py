#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo
from typing import List, Dict, Tuple
from helpers import helper as help
from genetic import algorithm as algo


def get_plot_color(index: int, cmap:str) -> str:
    return plt.cm.get_cmap(cmap)(index)


def efficient_frontier_plotter(risk_return_dicts_list: List[Dict[str, List]]):

    for index, risk_return_dict in enumerate(risk_return_dicts_list):
        plt.figure(2*index)
        stds = []
        returns = []
        for tup in list(risk_return_dict.values())[0]:
            stds.append(tup[0])
            returns.append(tup[1])
        plt.scatter(stds, returns, marker="X", label=list(risk_return_dict.keys())[0], color=get_plot_color(1+index*2, 'Paired'))
        #popt, pcov = spo.curve_fit(help.fitfun, stds, returns)


        t = np.linspace(min(stds), max(stds), 5000)
        #plt.plot(t, help.fitfun(np.array(t), *popt), '-', label='_nolegend_', color=get_plot_color(index*2, 'Paired'))
        plt.legend()
        plt.grid(True)
        plt.xlabel("Portfolio risk")
        plt.ylabel("Expected return")
        plt.title("Markowitz Model Efficient Frontiers")
        plt.savefig('./plots/frontier/'+str(help.get_num_files_in_dir('./plots/frontier/'))+'.png')

    return plt.show()


def plot_fitness_history(config: algo.Config, result: algo.AlgorithmResult):
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
    plt.savefig('./plots/fitnesshist/' + str(help.get_num_files_in_dir('./plots/fitnesshist/')) + '.png')


def plot_portfolio_history(config: algo.Config, result: algo.AlgorithmResult):
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
    plt.savefig('./plots/distrib/' + str(help.get_num_files_in_dir('./plots/distrib/')) + '.png')


def plot_solution(result: algo.AlgorithmResult):
    solution = result.get_solution()
    labels = solution.keys()
    sizes = solution.values()

    plt.figure()
    plt.title("Final portfolio distribution")
    plt.pie(sizes, labels=labels, autopct='%1.1f%%',
            startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('./plots/solution/' + str(help.get_num_files_in_dir('./plots/solution/')) + '.png')