#!/usr/bin/env python3
import multiprocessing
from typing import Dict, Any

Config = Dict[str, Any]  # definicja typu

config: Config = {
    # overall config
    'population_size' : 50,
    'max_runs': 200,

    # genetic config
    'mutation_probability': .1,
    'crossover_rate': .9,

    'mutation_gen_probability': .5,
    'mutation_coefficient': .01,

    'num_threads': multiprocessing.cpu_count(),
    'threading_enabled': True,
}