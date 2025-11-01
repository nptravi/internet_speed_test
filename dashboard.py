import streamlit as st
import analyzer

st.title("Internet Speed Test")
speedtest_result = analyzer.get_results()
col1, col2, col3 = st.columns(3)
col1.metric(label="Download Speed (Mbps)", value=speedtest_result["download_speeds"]["latest"],
          delta=round(speedtest_result["download_speeds"]["latest"]
                - speedtest_result["download_speeds"]["average"],2), border=True,
          chart_data = speedtest_result["download_speeds"]["values"])
col2.metric(label="Upload Speed (Mbps)", value=speedtest_result["upload_speeds"]["latest"],
          delta=round(speedtest_result["upload_speeds"]["latest"]
                - speedtest_result["upload_speeds"]["average"],2), border=True)
col3.metric(label="Ping (ms)", value=speedtest_result["ping_ms"]["latest"],
          delta=round(speedtest_result["ping_ms"]["latest"]
                - speedtest_result["ping_ms"]["average"],2), border=True)