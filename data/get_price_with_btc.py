#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import json
import time
from binance.client import Client

api_key = os.environ["API_KEY"]
api_secret = os.environ["API_SECRET"]

def get_price_with_btc(client:Client, coins:list[str], start: str, qty:str = "BTC"):
    for coin in coins:
        symbol = coin + qty
        filename = "{}.csv".format(symbol)
        with open(filename, "w") as csv_writer:
            writer = csv.writer(csv_writer)
            writer.writerow(["agg_trade_id", "price", "vol", "first_id", "last_id", "timestamp", "sell", "M"])
            agg_trades = client.aggregate_trade_iter(symbol, start_str=start)
            for trade in agg_trades:
                print(trade.values())
                writer.writerow(trade.values())
            time.sleep(1)


client = Client(api_key=api_key, api_secret=api_secret)
coins = None
with open("future_coins.json", mode="r") as f:
    data = f.read()
    coins = json.loads(data)

print(coins)
get_price_with_btc(client, coins, "July 14, 2017 UTC")
