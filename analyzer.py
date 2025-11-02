import os
from datetime import datetime
import pandas as pd

CSV_PATH = os.path.join("results", "speed_test_data.csv")

def get_results():
    dt = pd.read_csv(CSV_PATH, parse_dates=["timestamp"])
    dt['timestamp'] = pd.to_datetime(dt['timestamp'])
    latest = dt.sort_values(by=["timestamp"], ascending=True, inplace=False).iloc[-1].to_dict()
    latest["timestamp"] = latest["timestamp"]
    results = {"latest": latest,
        "download_speed": {
            "average": dt["download_speed"].mean(),
            "max": dt["download_speed"].max(),
            "min": dt["download_speed"].min(),
            "latest": dt["download_speed"].iloc[-1]},
        "upload_speed": {
            "average": dt["upload_speed"].mean(),
            "max": dt["upload_speed"].max(),
            "min": dt["upload_speed"].min(),
            "latest": dt["upload_speed"].iloc[-1]},
        "ping": {
            "average": dt["ping"].mean(),
            "max": dt["ping"].max(),
            "min": dt["ping"].min(),
            "latest": dt["ping"].iloc[-1],
            "values": dt[["timestamp", "ping"]]},
        "values": dt[["timestamp", "download_speed", "upload_speed", "ping","isp","server"]]
    }

    return results

if __name__ == "__main__":
    res = get_results()
    print(f"latest: {res['latest']}")
    print(f"download_speeds: {res['download_speed']}")
    print(f"upload_speeds: {res['upload_speed']}")
    print(f"ping_ms: {res['ping']}")
    print(f"values: {res['values']}")

