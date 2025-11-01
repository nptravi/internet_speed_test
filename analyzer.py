import os
from datetime import datetime
import pandas as pd

CSV_PATH = os.path.join("results", "speed_test_data.csv")

def get_lastest():
    dt = pd.read_csv(CSV_PATH, parse_dates=["timestamp"])
    latest = dt.sort_values(by=["timestamp"], ascending=False, inplace=False).iloc[0].to_dict()
    latest["timestamp"] = latest["timestamp"].to_pydatetime()
    return latest
def get_results():
    dt = pd.read_csv(CSV_PATH, parse_dates=["timestamp"])
    latest = dt.sort_values(by=["timestamp"], ascending=True, inplace=False).iloc[-1].to_dict()
    latest["timestamp"] = latest["timestamp"].to_pydatetime()
    results = {"latest": latest}
    download_speeds = dt.set_index("timestamp")["download_speed_mbps"].to_dict()
    upload_speeds = dt.set_index("timestamp")["upload_speed_mbps"].to_dict()
    ping_ms = dt.set_index("timestamp")["ping_ms"].to_dict()
    results["download_speeds"] = {
        "average": sum(download_speeds.values()) / len(download_speeds.values()),
        "max": max(download_speeds.values()),
        "min": min(download_speeds.values()),
        "latest": latest["download_speed_mbps"],
        "values": download_speeds.values()
    }
    results["upload_speeds"] = {
        "average": sum(upload_speeds.values()) / len(upload_speeds.values()),
        "max": max(upload_speeds.values()),
        "min": min(upload_speeds.values()),
        "latest": latest["upload_speed_mbps"]
    }
    results["ping_ms"] = {
        "average": sum(ping_ms.values()) / len(ping_ms.values()),
        "max": max(ping_ms.values()),
        "min": min(ping_ms.values()),
        "latest": latest["ping_ms"]
    }
    return results

if __name__ == "__main__":
    print(get_results())

