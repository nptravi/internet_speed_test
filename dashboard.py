import time
from datetime import datetime, timedelta
from inspect import stack
import pandas as pd
import streamlit as st
from dateutil.relativedelta import relativedelta
import analyzer
import altair as alt

@st.cache_data
def get_data(filter):
    today = datetime.today().date()
    from_date = None
    to_date = None
    match filter:
        case "All":
            from_date = datetime(2020, 1, 1).date()
            to_date = today
        case "Today":
            from_date = today
            to_date = today
        case "This Week":
            from_date = today - timedelta(days=7)
            to_date = today
        case "Last Week":
            from_date = today - timedelta(days=14)
            to_date = today - timedelta(days=7)
        case "This Month":
            from_date = today.replace(day=1)
            to_date = today
        case "Last Month":
            from_date = today.replace(day=1).replace(month=today.month - 1)
            to_date = today.replace(day=1) - timedelta(days=1)
        case "This Year":
            from_date = today.replace(day=1,month=1)
            to_date = today
        case "-":
            st.error("Filter selection value error")
    time.sleep(3)

    return analyzer.get_results(from_date, to_date)


st.set_page_config(layout="wide")

# Left panne for filter settings
left_pane,content_pane = st.columns([1,9])
left_pane.subheader("Settings")

left_pane.subheader("Filter Results")
selected_filter = left_pane.selectbox(label='For the past',
                                      options=['All','Today','This Week','Last Week',
                                               'This Month','Last Month', 'This Year'],
                                      accept_new_options=False,
                                      key='filter_box'
                                      )
speedtest_result = get_data(selected_filter)
if speedtest_result['status'] != 'success':
    st.error("Speedtest data request failed")
    st.stop()
elif speedtest_result['size'] == 0:
    st.warning(f"No test done during {selected_filter}")
    st.stop()

# Contents pane for displaying metrics, charts and data
content_pane.title("🌐 Internet Speed Monitoring")
content_pane.write("Track your internet performance over time")
content_pane.subheader("lastest Speed Test Result:")

col_metric_download, col_metric_upload, col_metric_ping_ms, col_test_count = (
    content_pane.columns(4))
col_metric_download.markdown("### ⬇️ Download Speed (Mbps)")
col_metric_download.metric(label="",
           value=speedtest_result["download_speed"]["latest"],
           delta=round(speedtest_result["download_speed"]["latest"]
                       - speedtest_result["download_speed"]["average"],2),
           chart_data = speedtest_result["data"][["timestamp","download_speed"]].set_index("timestamp"))
col_metric_upload.markdown("### ⬆️ Upload Speed (Mbps)")
col_metric_upload.metric(label="",
            value=speedtest_result["upload_speed"]["latest"],
            delta=round(speedtest_result["upload_speed"]["latest"]
                       - speedtest_result["upload_speed"]["average"],2),
            chart_data = speedtest_result["data"][["timestamp","upload_speed"]].set_index("timestamp"))
col_metric_ping_ms.markdown("### 📶 Ping (ms)")
col_metric_ping_ms.metric(label="",
            value=speedtest_result["ping"]["latest"],
            delta_color="inverse",
            delta=round(speedtest_result["ping"]["latest"]
                       - speedtest_result["ping"]["average"],2),
            chart_data = speedtest_result["data"][["timestamp","ping"]].set_index("timestamp"))
col_test_count.markdown("### 🔢 Tests Count")

col_test_count.metric(label="",
           value=speedtest_result["size"])

content_pane.write(f"ISP: {speedtest_result['latest']['isp']}")
content_pane.write(f"Server: {speedtest_result['latest']['server']}")
content_pane.write(f"last test: {speedtest_result['latest']['timestamp']}")

speed_dtf = speedtest_result["data"][['timestamp','download_speed','upload_speed']]
speed_dtf = speed_dtf.melt('timestamp', var_name="speed_type",value_name="speed")
base_chart_speed = alt.Chart(speed_dtf).encode(
    x=alt.X('timestamp:T',title='timestamp'),
    y=alt.Y('speed:Q', title='speed', stack='zero'),
    color=alt.Color('speed_type:N',scale=alt.Scale(range=['blue','brown'])),
    order=alt.Order('speed_type:N'))
area_chart_speed = (base_chart_speed.mark_area(opacity=0.4)
                    .encode(tooltip=['timestamp','speed','speed_type']))
point_chart_speed = (base_chart_speed.mark_point(filled=True, size=60)
                     .encode(tooltip=['timestamp','speed','speed_type']))
content_pane.subheader("Speed Chart")
content_pane.altair_chart(area_chart_speed + point_chart_speed, use_container_width=True,
                          on_select='ignore')

ping_dtf = speedtest_result["data"][['timestamp','ping']]
base_char_ping = alt.Chart(ping_dtf).encode(x='timestamp', y='ping')
area_chart_ping = (base_char_ping.mark_area(opacity=0.4)
                   .encode(tooltip=['timestamp','ping']))
point_chart_ping = (base_char_ping.mark_point(filled=True, size=60)
                    .encode(tooltip=['timestamp','ping']))
content_pane.subheader("Ping Chart")
content_pane.altair_chart(area_chart_ping + point_chart_ping, use_container_width=True,
                          on_select='ignore')

content_pane.subheader("Speed Test Data")
content_pane.dataframe(speedtest_result["data"],hide_index=True)