import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo
from typing import List, Dict, Tuple
import helpers as help

def get_plot_color(index: int, cmap:str) -> str:
    return plt.cm.get_cmap(cmap)(index)


def efficient_frontier_plotter(risk_return_dicts_list: List[Dict[str, List]]):

    for index, risk_return_dict in enumerate(risk_return_dicts_list):
        stds, returns = zip(*risk_return_dict.values())
        stds = list(map(list, stds))[0]
        returns = list(map(list,returns))[0]
        plt.scatter(stds, returns, marker="X", label=list(risk_return_dict.keys())[0], color=get_plot_color(1+index*2, 'Paired'))
        popt, pcov = spo.curve_fit(help.fitfun, stds, returns)
        t = np.arange(min(stds), max(stds), 0.1)
        plt.plot(t, help.fitfun(np.array(t), *popt), '-', label='_nolegend_', color=get_plot_color(index*2, 'Paired'))
        plt.legend()
        plt.grid(True)
        plt.xlabel("Portfolio risk")
        plt.ylabel("Expected return")
        plt.title("Markowitz Model Efficient Frontiers")
        plt.savefig('../plots/frontier'+str(help.get_num_files_in_dir('../plots/'))+'.png')

    return plt.show()

