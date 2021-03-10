import pandas as pd
import numpy as np

def readCrypto():
    dfBitcoin = pd.read_csv("datasets/crypto/bitcoin.csv", parse_dates=True, index_col=0)
    dfEthereum = pd.read_csv("datasets/crypto/ethereum.csv", parse_dates=True, index_col=0)
    dfLitecoin = pd.read_csv("datasets/crypto/litecoin.csv", parse_dates=True, index_col=0)
    dfXRP = pd.read_csv("datasets/crypto/xrp.csv", parse_dates=True, index_col=0)

    df = pd.DataFrame({'bitcoin': dfBitcoin['open'], 'ethereum': dfEthereum['open'], 'litecoin':dfLitecoin['open'], 'xrp':dfXRP['open']}, index=dfBitcoin['date'])
    return df

def calculateMean(dataframe):
    return dataframe.mean(axis=0, skipna=True)

def calculateSTD(dataframe):
    return dataframe.std(axis=0, skipna=True)

def calculateCovarianceMatrix(dataframe):
    return dataframe.cov()