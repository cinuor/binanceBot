#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import json
import time
from binance.client import Client

api_key = os.environ["API_KEY"]
api_secret = os.environ["API_SECRET"]

def get_price_with_btc(client:Client, coins:list[str], interval: str, start: str, qty:str = "BTC"):
    for coin in coins:
        symbol = coin + qty
        filename = "{}_{}.csv".format(symbol, interval)
        with open(filename, "w") as csv_writer:
            writer = csv.writer(csv_writer)
            writer.writerow(["open_ts", "open_price", "highest_price", "lowest_price", "close_price", "volume", "close_ts", "turnover", "trade_num", "buy_vol", "buy_turnover","ignore"])
            klines = client.get_historical_klines_generator(symbol, interval, start)
            for kline in klines:
                print(kline)
                writer.writerow(kline)
            time.sleep(1)


client = Client(api_key=api_key, api_secret=api_secret)
coins = None
with open("future_coins.json", mode="r") as f:
    data = f.read()
    coins = json.loads(data)

print(coins)
get_price_with_btc(client, coins, Client.KLINE_INTERVAL_15MINUTE, "July 14, 2017 UTC")
