import os
from datetime import datetime
import pandas as pd

CSV_PATH = os.path.join("results", "speed_test_data.csv")

def get_lastest():
    dt = pd.read_csv(CSV_PATH, parse_dates=["timestamp"])
    latest = dt.sort_values(by=["timestamp"], ascending=False, inplace=False).iloc[0].to_dict()
    latest["timestamp"] = latest["timestamp"].to_pydatetime()
    return latest

if __name__ == "__main__":
    print(get_lastest())

