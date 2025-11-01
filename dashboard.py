import streamlit as st
import analyzer
import speed_tester


def check_now():
    placeholder = st.empty()
    with placeholder.container():
        st.image(image="images/spinner.gif",caption="Speed test in progress...")
        st.markdown("## Testing internet speed, please wait...")
        speed_tester.speed_test()
    placeholder.empty()  # remove spinner
    st.success("✅ Speed test completed!")


speedtest_result = analyzer.get_results()

st.set_page_config(layout="wide")
# Left panne for filter settings
left_pane,content_pane = st.columns([1,9])
left_pane.subheader("Settings")

left_pane.write("Filter settings will be added here")

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
col_test_count.button(label="Check now", key="check_now", on_click=check_now)
content_pane.write(f"ISP: {speedtest_result['latest']['isp']}")
content_pane.write(f"Server: {speedtest_result['latest']['server']}")
content_pane.write(f"last test: {speedtest_result['latest']['timestamp']}")

speed_dtf = speedtest_result["values"][['timestamp','download_speed','upload_speed']].set_index('timestamp')
content_pane.subheader("Speed Chart")
content_pane.area_chart(data=speed_dtf,x_label="Timestamp",y_label="Speed (Mbps)")