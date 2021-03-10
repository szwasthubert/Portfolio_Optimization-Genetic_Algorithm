import pandas as pd

def readCrypto():
    dfBitcoin = pd.read_csv("data/crypto/bitcoin.csv", parse_dates=True)
    dfEtherum = pd.read_csv("data/crypto/etherum.csv", parse_dates=True)
    dfLitecoin = pd.read_csv("data/crypto/litecoin.csv", parse_dates=True)
    dfXRP = pd.read_csv("data/crypto/xrp.csv", parse_dates=True)

    return pd.DataFrame({'bitcoin': dfBitcoin['open'], 'ethereum': dfEtherum['open'], 'litecoin':dfLitecoin['open'], 'xrp':dfXRP['open']})

def convertClosesToReturns(dataframe):
    return dataframe.diff().drop([0], axis='rows')

def returnCorrelationMatrix(covDataframe, stdDataframe):

    corrMatrix = covDataframe.copy()

    for colname in corrMatrix.columns:
        corrMatrix[colname] /= stdDataframe[colname]

    for rowname in corrMatrix.index.values:
        corrMatrix.loc[rowname] /= stdDataframe[rowname]

    return corrMatrix