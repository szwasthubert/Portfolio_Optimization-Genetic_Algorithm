#!/usr/bin/env python3

def calculateMean(dataframe):
    return dataframe.mean(axis=0, skipna=True)


def calculateStd(dataframe):
    return dataframe.std(axis=0, skipna=True)


def calculateCovarianceMatrix(dataframe):
    return dataframe.cov()


def expectedPortfolioReturn(portfolioWeightsDict, meanReturnsDataset):
    expectedReturn = 0
    for key, value in portfolioWeightsDict.items():
        expectedReturn += value * meanReturnsDataset[key]
    return expectedReturn


def portfolioStd(portfolioWeightsDict, covarianceDataset):
    n = len(portfolioWeightsDict)
    portfolioKeys = portfolioWeightsDict.keys()
    variance = 0
    for key, value in portfolioWeightsDict.items():
        variance += covarianceDataset.loc[key][key] * value ** 2

    for i in range(n):
        for j in range(i + 1, n + 1):
            variance += 2 * portfolioWeightsDict[portfolioKeys[i]] * portfolioWeightsDict[portfolioKeys[j]] * \
                        covarianceDataset.iloc[portfolioKeys[i]][portfolioKeys[j]]

    return math.sqrt(variance)
