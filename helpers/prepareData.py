import pandas as pd
import numpy as np

def readCrypto():
    dfBitcoin = pd.read_csv("../datasets/crypto/bitcoin.csv", parse_dates=True, index_col=0)
    dfEtherum = pd.read_csv("../datasets/crypto/etherum.csv", parse_dates=True, index_col=0)
    dfLitecoin = pd.read_csv("../datasets/crypto/litecoin.csv", parse_dates=True, index_col=0)
    dfXRP = pd.read_csv("../datasets/crypto/xrp.csv", parse_dates=True, index_col=0)

    df = pd.DataFrame({'bitcoin': dfBitcoin['open'], 'ethereum': dfEtherum['open'], 'litecoin':dfLitecoin['open'], 'xrp':dfXRP['open']}, index=dfBitcoin.index)
    return df