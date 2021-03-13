#!/usr/bin/env python3

import pandas as pd
from typing import List

def parse_crypto():
    df_bitcoin = pd.read_csv("../raw_data/crypto/bitcoin.csv", parse_dates=True, index_col=0)
    df_etherum = pd.read_csv("../raw_data/crypto/etherum.csv", parse_dates=True, index_col=0)
    df_litecoin = pd.read_csv("../raw_data/crypto/litecoin.csv", parse_dates=True, index_col=0)
    df_XRP = pd.read_csv("../raw_data/crypto/xrp.csv", parse_dates=True, index_col=0)

    pd.DataFrame({'bitcoin': df_bitcoin['open'],
                    'ethereum': df_etherum['open'],
                    'litecoin':df_litecoin['open'],
                    'xrp':df_XRP['open']},
                index=df_bitcoin.index).to_csv("../data/crypto.csv")


def parse_investing(type: str, names: List):
    (pd.DataFrame({name: pd.read_csv(f"../raw_data/{type}/{name}.csv", parse_dates=True, index_col=0)['Open'] for name in names})).to_csv(f"../data/{type}.csv")


parse_crypto()

investments = {"commodities": ["gold", "silver", "platinum", "oil"],
	       "currencies": ["USD_CHF", "USD_CNY", "USD_EUR", "USD_GBP", "USD_PLN"],
	       "indices": ["DAX", "Dow Jones", "NASDAQ Composite", "S&P 500"]}

for type, names in investments.items():
	parse_investing(type, names)
