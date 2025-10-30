import time
import speedtest

start_time = time.time()
st = speedtest.Speedtest(secure=True)
#st.get_best_server()
print("Testing download speed...")
down_speed = st.download()
print("Testing upload speed...")
up_speed = st.upload()
print(f"""Download Speed: {down_speed} Mbps
Upload Speed: {st.results.upload} Mbps
result: {st.results}""")
st_results = st.results.dict()
dt= {"timestamp": st_results["timestamp"],
     "download_speed": st_results["download"],
     "upload_speed": st_results["upload"],
     "ping_ms": st_results["ping"],
     "server_name": st_results["server"]["sponsor"],
     "server_location": f"""{st_results["server"]["name"]}, {st_results["server"]["country"]}""",
     "bytes_sent": st_results["bytes_sent"],
     "bytes_received": st_results["bytes_received"]}

print(f"dt={dt}")





# time stamp, download_speed, upload_speed, ping_ms, server_name, server_location, isp


