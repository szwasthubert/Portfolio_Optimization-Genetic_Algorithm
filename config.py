from typing import Dict, Any

Config = Dict[str, Any]  # definicja typu

config: Config = {
    # overall config
    'population_size' : 20,
    'max_runs': 500,

    'max_gain_value' : 1,
    'max_integral_value': 1,
    'max_derivative_value': 1,

    # genetic config
    'mutation_probability': .1,
    'crossover_rate': .9,
}