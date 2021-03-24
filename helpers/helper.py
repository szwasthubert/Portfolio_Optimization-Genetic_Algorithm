#!/usr/bin/env python3

import numpy as np
import pandas as pd
import os
from typing import Dict, List, Tuple


def calculate_diff(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.diff().dropna()


def calculate_mean(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.mean(skipna=True)


def calculate_std(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.std(skipna=True)


def calculate_normalized_covariance_matrix(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.corr()


def calculate_RV(dataframe: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    dataframe = calculate_diff(dataframe)
    return calculate_mean(dataframe), calculate_normalized_covariance_matrix(dataframe)


def expected_portfolio_return(portfolioWeightsDict: Dict, meanReturnsDataset: pd.DataFrame) -> float:
    expectedReturn = 0
    for key, value in portfolioWeightsDict.items():
        expectedReturn += value * meanReturnsDataset[key]
    return expectedReturn


def portfolio_std(portfolioWeightsDict: Dict, covarianceDataset: pd.DataFrame) -> float:
    n = len(portfolioWeightsDict)
    portfolioKeys = list(portfolioWeightsDict.keys())
    variance = 0
    for key, value in portfolioWeightsDict.items():
        variance += covarianceDataset.loc[key][key] * (value ** 2)

    for i in range(n-1):
        for j in range(i+1, n):
            variance += 2 * portfolioWeightsDict[portfolioKeys[i]] * portfolioWeightsDict[portfolioKeys[j]] * \
                        covarianceDataset.loc[portfolioKeys[i]][portfolioKeys[j]]

    return variance


def risk_return_dict_generator(instrumentSet: str, portfolioWeightsDicts: List[Dict], meanReturnsDataset: pd.DataFrame,
                               covarianceDataset: pd.DataFrame) -> Dict[str, List[Tuple]]:
    return {instrumentSet: [(portfolio_std(portfolioWeightsDict, covarianceDataset),
                             expected_portfolio_return(portfolioWeightsDict, meanReturnsDataset)) for
                            portfolioWeightsDict in portfolioWeightsDicts]}


def fitfun(x, a, b, c, d):
    return d + a/(b*x+c)


def get_num_files_in_dir(path: str) -> int:
    if not os.path.exists(path):
        os.makedirs(path)
    return len([name for name in os.listdir(path) if os.path.isfile(name)])
