import os
import csv
import fire
import datetime
from binance.client import Client
from binance.enums import HistoricalKlinesType

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
    "1M": Client.KLINE_INTERVAL_1MONTH,
}


def timestamp(time_str: str) -> int:
    ts = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000
    return int(round(ts))


class Inquirer:
    def __init__(self, client: Client):
        self.client = client

    def spot(self, symbol: str, start: str, end: str, interval: str) -> None:
        filename = "{}_{}.csv".format(symbol, interval)
        try:
            klines = self.client.get_historical_klines_generator(
                symbol,
                INTERVAL[interval],
                timestamp(start),
                timestamp(end),
                klines_type=HistoricalKlinesType.SPOT,
            )
            with open(filename, "w") as csv_writer:
                writer = csv.writer(csv_writer)
                writer.writerow(
                    [
                        "open_ts",
                        "open_price",
                        "highest_price",
                        "lowest_price",
                        "close_price",
                        "volume",
                        "close_ts",
                        "turnover",
                        "trade_num",
                        "buy_vol",
                        "buy_turnover",
                        "ignore",
                    ]
                )
                for kline in klines:
                    writer.writerow(kline)
        except Exception as e:
            raise e

    def future(self, symbol: str, start: str, end: str, interval: str) -> None:
        filename = "{}_future_{}.csv".format(symbol, interval)
        try:
            klines = self.client.get_historical_klines_generator(
                symbol,
                INTERVAL[interval],
                timestamp(start),
                timestamp(end),
                klines_type=HistoricalKlinesType.FUTURES,
            )
            with open(filename, "w") as csv_writer:
                writer = csv.writer(csv_writer)
                writer.writerow(
                    [
                        "open_ts",
                        "open_price",
                        "highest_price",
                        "lowest_price",
                        "close_price",
                        "volume",
                        "close_ts",
                        "turnover",
                        "trade_num",
                        "buy_vol",
                        "buy_turnover",
                        "ignore",
                    ]
                )
                for kline in klines:
                    writer.writerow(kline)
        except Exception as e:
            raise e


if __name__ == "__main__":
    inquirer = Inquirer(Client(api_key=api_key, api_secret=api_secret))
    fire.Fire(inquirer)
