#!/usr/bin/env python3

import pandas as pd
from typing import List
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

def parse_crypto():
    data_path = os.path.join(SCRIPT_PATH, "../data/")

    df_bitcoin = pd.read_csv(os.path.join(SCRIPT_PATH, "../raw_data/crypto/bitcoin.csv"), 
                             parse_dates=True, 
                             index_col=0)
    df_etherum = pd.read_csv(os.path.join(SCRIPT_PATH, "../raw_data/crypto/etherum.csv"), 
                             parse_dates=True, 
                             index_col=0)
    df_litecoin = pd.read_csv(os.path.join(SCRIPT_PATH, "../raw_data/crypto/litecoin.csv"), 
                              parse_dates=True, 
                              index_col=0)
    df_XRP = pd.read_csv(os.path.join(SCRIPT_PATH, "../raw_data/crypto/xrp.csv"), 
                         parse_dates=True, 
                         index_col=0)

    if not os.path.isdir(data_path):
        os.os.mkdir(data_path)

    pd.DataFrame({'bitcoin': df_bitcoin['open'], 
                  'ethereum': df_etherum['open'], 
                  'litecoin':df_litecoin['open'], 
                  'xrp':df_XRP['open']}, 
                index=df_bitcoin.index).to_csv(os.path.join(data_path, "crypto.csv"))

def parse_investing(type: str, names: List):
    data_path = os.path.join(SCRIPT_PATH, "../data/")
    df = pd.DataFrame({name: pd.read_csv(os.path.join(SCRIPT_PATH, 
                                         f"../raw_data/{type}/{name}.csv"), 
    		          parse_dates=True, 
    		          index_col=0,
                      thousands=',')['Open'] for name in names})
    if not os.path.isdir(data_path):
        os.os.mkdir(data_path)
    df.fillna(method="ffill").fillna(method="bfill").to_csv(os.path.join(data_path, 
                                                                         f"{type}.csv"))


if __name__ == "__main__":

    parse_crypto()
    investments = {"commodities": ["gold", "silver", "platinum", "oil"],
                   "currencies": ["USD_CHF", "USD_CNY", "USD_EUR", "USD_GBP", "USD_PLN"],
                   "indices": ["DAX", "Dow Jones", "NASDAQ Composite", "S&P 500"]}

    for type, names in investments.items():
	    parse_investing(type, names)

