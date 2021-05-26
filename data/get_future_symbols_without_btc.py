#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  获取除了BTC的U本位symbols列表

import json
import os
from binance.client import Client

api_key=os.environ["API_KEY"]
api_secret=os.environ["API_SECRET"]

def get_symbol_in_future(client:Client, qty: str = "USDT") -> list[str]:
    f_info = client.futures_exchange_info()
    return [item["baseAsset"] for item in f_info["symbols"] if item["symbol"].endswith(qty) and item["baseAsset"] != "BTC"]

client = Client(api_key=api_key, api_secret=api_secret)
symbols = get_symbol_in_future(client)
with open("future_coins.json", mode="w") as f:
    data = json.dumps(symbols, indent=2)
    f.write(data)
