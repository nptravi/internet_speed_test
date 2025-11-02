from datetime import datetime, timedelta
from inspect import stack

import pandas as pd
import streamlit as st
from dateutil.relativedelta import relativedelta

import analyzer
import speed_tester
import altair as alt
import socket

speedtest_result = analyzer.get_results()
speedtest_data = speedtest_result['values']
selected_filter = 'ALL'

def check_now():
    global selected_filter, speedtest_data, speedtest_result
    placeholder = st.empty()
    with placeholder.container():
        st.image(image="images/spinner.gif",caption="Speed test in progress...")
        st.markdown("## Testing internet speed, please wait...")
        speed_tester.speed_test()
        speedtest_result = analyzer.get_results()
        speedtest_data = speedtest_result['values']
        selected_filter = st.session_state['filter_box']
    placeholder.empty()  # remove spinner
    st.success("✅ Speed test completed!")


def apply_filter():
    global speedtest_result, speedtest_data, selected_filter
    if st.session_state['filter_box']:
        selected_filter = st.session_state["filter_box"]
    else:
        selected_filter = "ALL"
    speedtest_result = analyzer.get_results()
    speedtest_data = speedtest_result['values']
    selected_filter = st.session_state["filter_box"]
    today = datetime.today().date()
    match selected_filter:
        case "ALL":
            pass
        case "Today":
            speedtest_data = speedtest_data[speedtest_data['timestamp'].dt.date >= today]
            speedtest_result['values'] = speedtest_data
        case "This Week":
            from_date = today - timedelta(weeks=1)
            speedtest_data = speedtest_data[speedtest_data['timestamp'].dt.date >= from_date]
            speedtest_result['values'] = speedtest_data
        case "Last Week":
            from_date = today - timedelta(weeks=2)
            to_date = today - timedelta(weeks=1)
            speedtest_data = speedtest_data[(speedtest_data['timestamp'].dt.date >= from_date) &
                                            (speedtest_data['timestamp'].dt.date < to_date)]
            speedtest_result['values'] = speedtest_data
        case "This Month":
            from_date = today.replace(day=1)
            speedtest_data = speedtest_data[speedtest_data['timestamp'].dt.date >= from_date]
            speedtest_result['values'] = speedtest_data
        case "Last Month":
            from_date = today.replace(day=1).replace(month=today.month-1)
            to_date = from_date + relativedelta(months=1)
            speedtest_data = speedtest_data[(speedtest_data['timestamp'].dt.date >= from_date) &
                                            (speedtest_data['timestamp'].dt.date < to_date)]
            speedtest_result['values'] = speedtest_data


st.set_page_config(layout="wide")
# Left panne for filter settings
left_pane,content_pane = st.columns([1,9])
left_pane.subheader("Settings")

left_pane.subheader("Filter Results")
left_pane.selectbox(label='For the past',
                                      options=['All','Today','This Week','Last Week',
                                               'This Month','Last Month', 'This Year'],
                                      on_change=apply_filter,
                                      accept_new_options=False,
                                      key='filter_box'
                                      )
apply_filter()

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
           chart_data = speedtest_result["values"][["timestamp","download_speed"]].set_index("timestamp"))
col_metric_upload.markdown("### ⬆️ Upload Speed (Mbps)")
col_metric_upload.metric(label="",
            value=speedtest_result["upload_speed"]["latest"],
            delta=round(speedtest_result["upload_speed"]["latest"]
                       - speedtest_result["upload_speed"]["average"],2),
            chart_data = speedtest_result["values"][["timestamp","upload_speed"]].set_index("timestamp"))
col_metric_ping_ms.markdown("### 📶 Ping (ms)")
col_metric_ping_ms.metric(label="",
            value=speedtest_result["ping"]["latest"],
            delta_color="inverse",
            delta=round(speedtest_result["ping"]["latest"]
                       - speedtest_result["ping"]["average"],2),
            chart_data = speedtest_result["values"][["timestamp","ping"]].set_index("timestamp"))
col_test_count.markdown("### 🔢 Tests Count")
# col_test_count.markdown(" ###")
#col_test_count.markdown(f"<div style='text-align: center; font-size: 64px; border: 1px solid lightgray'>{speedtest_result['download_speeds']['values']['timestamp'].count()}</div>",
#                        unsafe_allow_html=True)

col_test_count.metric(label="",
           value=speedtest_result["values"][["timestamp"]].count())
host_name = socket.gethostbyname(socket.gethostname())
is_localhost = host_name.startswith("localhost") or host_name.startswith("127.0.0.1")
if is_localhost:
    col_test_count.button(label="Check now", key="check_now", on_click=check_now)
content_pane.write(f"ISP: {speedtest_result['latest']['isp']}")
content_pane.write(f"Server: {speedtest_result['latest']['server']}")
content_pane.write(f"last test: {speedtest_result['latest']['timestamp']}")

speed_dtf = speedtest_result["values"][['timestamp','download_speed','upload_speed']]
speed_dtf = speed_dtf.melt('timestamp', var_name="speed_type",value_name="speed")
base_chart_speed = alt.Chart(speed_dtf).encode(
    x=alt.X('timestamp:T',title='timetamp'),
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

ping_dtf = speedtest_result["values"][['timestamp','ping']]
base_char_ping = alt.Chart(ping_dtf).encode(x='timestamp', y='ping')
area_chart_ping = (base_char_ping.mark_area(opacity=0.4)
                   .encode(tooltip=['timestamp','ping']))
point_chart_ping = (base_char_ping.mark_point(filled=True, size=60)
                    .encode(tooltip=['timestamp','ping']))
content_pane.subheader("Ping Chart")
content_pane.altair_chart(area_chart_ping + point_chart_ping, use_container_width=True,
                          on_select='ignore')

content_pane.subheader("Speed Test Data")
content_pane.dataframe(speedtest_data,hide_index=True)