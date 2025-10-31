import csv
from datetime import datetime
import speedtest
import os

def speed_test():
    """ Runs internet speed tests (download and then upload)
    Store the result in speed_test_data.csv
    """
    start_time = datetime.now()
    st = speedtest.Speedtest(secure=True)
    print("Testing download speed...")
    down_speed = st.download()/1000000.0
    down_speed = round(down_speed, 2)
    print("Testing upload speed...")
    up_speed = st.upload()/1000000.0
    up_speed = round(up_speed, 2)
    print(f"""Download Speed: {down_speed} Mbps
    Upload Speed: {up_speed} Mbps
    result: {st.results}""")
    st_results = st.results.dict()

    dt= {"timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S"),
         "download_speed_mbps": down_speed,
         "upload_speed_mbps": up_speed,
         "ping_ms": st_results["ping"],
         "server_name": st_results["server"]["sponsor"],
         "server_location": f"""{st_results["server"]["name"]} - {st_results["server"]["country"]}""",
         "bytes_sent": st_results["bytes_sent"],
         "bytes_received": st_results["bytes_received"]}
    csv_file_name =os.path.join("results","speed_test_data.csv")
    file_exists = os.path.isfile(csv_file_name)
    with open(csv_file_name, "a") as f:
        writer = csv.DictWriter(f,fieldnames=dt.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(dt)

if __name__ == "__main__":
    speed_test()





# time stamp, download_speed, upload_speed, ping_ms, server_name, server_location, isp


