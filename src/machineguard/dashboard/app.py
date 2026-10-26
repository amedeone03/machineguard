import altair as alt
import streamlit as st

from machineguard.dashboard.data import load_measurements


ANOMALY_THRESHOLD = -0.06108184766069839


st.set_page_config(
    page_title="MachineGuard",
    page_icon="⚙️",
    layout="wide",
)


st.title("MachineGuard")
st.subheader("Predictive Maintenance Dashboard")

st.write(
    "Monitoring bearing condition using NASA IMS vibration data."
)


measurements = load_measurements()


# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------

st.sidebar.header("Filters")

min_date = measurements["timestamp"].min().date()
max_date = measurements["timestamp"].max().date()

selected_dates = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)


if len(selected_dates) == 2:
    start_date, end_date = selected_dates

    filtered_measurements = measurements[
        measurements["timestamp"]
        .dt.date
        .between(
            start_date,
            end_date,
        )
    ]
else:
    filtered_measurements = measurements


# ---------------------------------------------------------
# Current bearing health
# Always based on latest measurement in full dataset
# ---------------------------------------------------------

latest_measurement = measurements.iloc[-1]

latest_score = latest_measurement["anomaly_score"]
latest_rms = latest_measurement["rms"]
latest_flag = latest_measurement["anomaly_flag"]


if latest_flag:
    current_status = "CRITICAL"
else:
    current_status = "NORMAL"


st.subheader("Current bearing health")

health_col1, health_col2, health_col3 = st.columns(3)

health_col1.metric(
    label="Current status",
    value=current_status,
)

health_col2.metric(
    label="Latest anomaly score",
    value=f"{latest_score:.4f}",
)

health_col3.metric(
    label="Latest RMS",
    value=f"{latest_rms:.4f}",
)


st.divider()


# ---------------------------------------------------------
# Selected period summary
# ---------------------------------------------------------

st.subheader("Selected period summary")

total_measurements = len(filtered_measurements)

anomalous_measurements = int(
    filtered_measurements["anomaly_flag"]
    .fillna(False)
    .sum()
)

anomaly_percentage = (
    anomalous_measurements / total_measurements * 100
    if total_measurements > 0
    else 0
)

if not filtered_measurements.empty:
    minimum_anomaly_score = (
        filtered_measurements["anomaly_score"].min()
    )
else:
    minimum_anomaly_score = None


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Measurements",
    value=total_measurements,
)

col2.metric(
    label="Anomalous measurements",
    value=anomalous_measurements,
)

col3.metric(
    label="Anomaly rate",
    value=f"{anomaly_percentage:.1f}%",
)

col4.metric(
    label="Minimum anomaly score",
    value=(
        f"{minimum_anomaly_score:.4f}"
        if minimum_anomaly_score is not None
        else "N/A"
    ),
)


# ---------------------------------------------------------
# RMS chart
# ---------------------------------------------------------

st.subheader("RMS vibration over time")

if filtered_measurements.empty:
    st.info(
        "No measurements are available for the selected date range."
    )
else:
    st.line_chart(
        filtered_measurements,
        x="timestamp",
        y="rms",
    )


# ---------------------------------------------------------
# Anomaly score chart
# ---------------------------------------------------------

st.subheader("Anomaly score over time")

anomaly_data = filtered_measurements.dropna(
    subset=["anomaly_score"]
).copy()


if anomaly_data.empty:
    st.info(
        "No anomaly scores are available for the selected date range."
    )

else:
    score_line = (
        alt.Chart(anomaly_data)
        .mark_line()
        .encode(
            x=alt.X(
                "timestamp:T",
                title="Timestamp",
            ),
            y=alt.Y(
                "anomaly_score:Q",
                title="Anomaly score",
            ),
            tooltip=[
                alt.Tooltip(
                    "timestamp:T",
                    title="Timestamp",
                ),
                alt.Tooltip(
                    "anomaly_score:Q",
                    title="Anomaly score",
                    format=".4f",
                ),
            ],
        )
    )

    anomalous_points = (
        alt.Chart(
            anomaly_data[
                anomaly_data["anomaly_flag"] == True
            ]
        )
        .mark_circle(
            size=35
        )
        .encode(
            x=alt.X(
                "timestamp:T",
                title="Timestamp",
            ),
            y=alt.Y(
                "anomaly_score:Q",
                title="Anomaly score",
            ),
            tooltip=[
                alt.Tooltip(
                    "timestamp:T",
                    title="Timestamp",
                ),
                alt.Tooltip(
                    "anomaly_score:Q",
                    title="Anomaly score",
                    format=".4f",
                ),
            ],
        )
    )

    threshold_line = (
        alt.Chart(
            {
                "values": [
                    {
                        "threshold": ANOMALY_THRESHOLD
                    }
                ]
            }
        )
        .mark_rule(
            strokeDash=[6, 4]
        )
        .encode(
            y=alt.Y(
                "threshold:Q",
                title="Anomaly score",
            )
        )
    )

    anomaly_chart = (
        score_line
        + anomalous_points
        + threshold_line
    ).properties(
        height=400
    )

    st.altair_chart(
        anomaly_chart,
        use_container_width=True,
    )

    st.caption(
        f"Anomaly threshold: {ANOMALY_THRESHOLD:.4f}. "
        "Scores below the threshold are classified as anomalous."
    )


# ---------------------------------------------------------
# Recent measurements
# ---------------------------------------------------------

st.subheader("Recent measurements")

st.dataframe(
    filtered_measurements.tail(20),
    use_container_width=True,
)