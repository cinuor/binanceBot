#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import csv
import json
import time
from binance.client import Client

api_key = os.environ["API_KEY"]
api_secret = os.environ["API_SECRET"]

INTERVAL = {
    "1m": Client.KLINE_INTERVAL_1MINUTE,
    "3m": Client.KLINE_INTERVAL_3MINUTE,
    "5m": Client.KLINE_INTERVAL_5MINUTE,
    "15m": Client.KLINE_INTERVAL_15MINUTE,
    "30m": Client.KLINE_INTERVAL_30MINUTE,
    "1h": Client.KLINE_INTERVAL_1HOUR,
    "2h": Client.KLINE_INTERVAL_2HOUR,
    "4h": Client.KLINE_INTERVAL_4HOUR,
    "6h": Client.KLINE_INTERVAL_6HOUR,
    "8h": Client.KLINE_INTERVAL_8HOUR,
    "12h": Client.KLINE_INTERVAL_12HOUR,
    "1d": Client.KLINE_INTERVAL_1DAY,
    "3d": Client.KLINE_INTERVAL_3DAY,
    "1w": Client.KLINE_INTERVAL_1DAY,
    "1M": Client.KLINE_INTERVAL_1MONTH
}

def get_price_with_btc(client:Client, coins:list[str], interval: str, start: str, qty:str = "USDT"):
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

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help", "help"]:
        print("usage: python get_price_with_btc.py INTERVAL QTY")
        print("for example: python get_price_with_btc.py 15m BTC")
        sys.exit(0)
    else:
        client = Client(api_key=api_key, api_secret=api_secret)
        coins = None
        with open("future_coins.json", mode="r") as f:
            data = f.read()
            coins = json.loads(data)
            print(sorted(coins))
        get_price_with_btc(client, sorted(coins), INTERVAL[str(sys.argv[1])], "July 14, 2017 UTC",qty=str(sys.argv[2]))

