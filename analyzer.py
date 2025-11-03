import os
from datetime import datetime
import pandas as pd

CSV_PATH = os.path.join("results", "speed_test_data.csv")

def get_results(from_date=datetime(2024,1,1).date(),
                to_date=datetime.today().date()):
    try:
        dt = pd.read_csv(CSV_PATH, parse_dates=["timestamp"])
        dt['timestamp'] = pd.to_datetime(dt['timestamp'])
        latest = dt.sort_values(by=["timestamp"], ascending=True, inplace=False).iloc[-1].to_dict()
        dt = dt[(dt['timestamp'].dt.date >= from_date) & (dt['timestamp'].dt.date <= to_date)]
        if len(dt) == 0:
            return {"status": "success", "size":0}
        results = {
            "status": "success",
            "size": len(dt),
            "latest": latest,
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
            "data": dt[["timestamp", "download_speed", "upload_speed", "ping","isp","server"]]
        }
        return results
    except Exception as e:
        print(e)
        return {"status": 'error'}

if __name__ == "__main__":
    res = get_results()
    print(res)
    #(f"latest: {res['latest']}")
    #print(f"download_speeds: {res['download_speed']}")
    #print(f"upload_speeds: {res['upload_speed']}")
    #print(f"ping_ms: {res['ping']}")
    #print(f"values: {res['data']}")

