import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import time

# Project modules
from risk_engine import (
    load_data,
    prepare_features,
    train_model,
    detect_anomalies,
    add_zone_detection,
    add_risk_scores
)
from data_processor import clean_data, create_features

# ----------------------------
# DARK RADAR STYLE
# ----------------------------
st.set_page_config(page_title="AI Airspace Command Center", layout="wide")

st.markdown("""
<style>
body {
    background-color: #0b0f1a;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("AI Airspace Surveillance & Threat Detection System")
st.markdown("### Real-Time AI Command Dashboard")

# ----------------------------
# LOAD DATA
# ----------------------------
df = load_data()
df = clean_data(df)
df = create_features(df)

features = prepare_features(df)
model = train_model(features)
df = detect_anomalies(model, features, df)
df = add_zone_detection(df)
df = add_risk_scores(df)

# ----------------------------
# SIMULATION SETTINGS
# ----------------------------
num_steps = 100
move_speed = 0.001
sleep_time = 0.5

# ----------------------------
# TRACK POSITIONS + TRAJECTORY
# ----------------------------
positions = df[["latitude", "longitude"]].copy()

trajectory_history = {
    aid: [(lat, lon)]
    for aid, lat, lon in zip(df["aircraft_id"], df["latitude"], df["longitude"])
}

# ----------------------------
# LAYOUT
# ----------------------------
col_map, col_side = st.columns([3, 1])

# ----------------------------
# SIDE PANEL – THREAT SUMMARY
# ----------------------------
col_side.subheader("Threat Classification")

metric_total = col_side.empty()
metric_normal = col_side.empty()
metric_anomaly = col_side.empty()
metric_high = col_side.empty()

alerts_placeholder = col_side.empty()
table_placeholder = col_side.empty()

# ----------------------------
# MAP PLACEHOLDER
# ----------------------------
map_placeholder = col_map.empty()

# ----------------------------
# ANALYTICS SECTION
# ----------------------------
st.subheader("Airspace Intelligence Analytics")

chart_placeholder = st.empty()
scatter_placeholder = st.empty()

# ----------------------------
# PYDECK LAYERS
# ----------------------------
def get_aircraft_layer(df):

    df_copy = df.copy()

    def color_map(risk):
        if risk == 10:
            return [0,255,0]
        elif risk == 60:
            return [255,165,0]
        else:
            return [255,0,0]

    df_copy["color"] = df_copy["risk_score"].apply(color_map)

    return pdk.Layer(
        "ScatterplotLayer",
        data=df_copy,
        get_position=["longitude","latitude"],
        get_color="color",
        get_radius=300,
        pickable=True
    )

def get_trajectory_layer(history):

    line_data = []

    for aid, coords in history.items():
        if len(coords) < 2:
            continue

        line_data.append({
            "path": [(lon, lat) for lat, lon in coords],
            "color": [0, 150, 255]
        })

    return pdk.Layer(
        "LineLayer",
        data=pd.DataFrame(line_data),
        get_path="path",
        get_color="color",
        get_width=2
    )

def get_restricted_layer():

    return pdk.Layer(
        "PolygonLayer",
        data=[{
            "polygon": [
                [-13.25,8.45],
                [-13.20,8.45],
                [-13.20,8.50],
                [-13.25,8.50]
            ]
        }],
        get_polygon="polygon",
        get_fill_color=[255,0,0,40]
    )

# ----------------------------
# MAP VIEW
# ----------------------------
view_state = pdk.ViewState(
    latitude=8.48,
    longitude=-13.22,
    zoom=11
)

deck = pdk.Deck(
    layers=[],
    initial_view_state=view_state,
    tooltip={"text": "Aircraft {aircraft_id}\nRisk Level: {risk_score}"}
)

# ----------------------------
# MAIN LOOP
# ----------------------------
for step in range(num_steps):

    # Move aircraft
    positions["latitude"] += np.random.uniform(-move_speed, move_speed, len(df))
    positions["longitude"] += np.random.uniform(-move_speed, move_speed, len(df))

    df["latitude"] = positions["latitude"]
    df["longitude"] = positions["longitude"]

    # Update intelligence
    df = add_zone_detection(df)
    df = add_risk_scores(df)

    # Update trajectory
    for _, row in df.iterrows():
        trajectory_history[row["aircraft_id"]].append(
            (row["latitude"], row["longitude"])
        )

    # Map layers
    layers = [
        get_restricted_layer(),
        get_aircraft_layer(df),
        get_trajectory_layer(trajectory_history)
    ]

    deck.layers = layers

    map_placeholder.pydeck_chart(deck)

    # ----------------------------
    # THREAT CLASSIFICATION
    # ----------------------------
    total = len(df)
    normal = len(df[df["risk_score"] == 10])
    anomaly = len(df[df["risk_score"] == 60])
    high = len(df[df["risk_score"] == 95])

    metric_total.metric("Total Aircraft", total)
    metric_normal.metric("Normal Aircraft", normal)
    metric_anomaly.metric("Suspicious Aircraft", anomaly)
    metric_high.metric("High-Threat Aircraft", high)

    # ----------------------------
    # ALERTS
    # ----------------------------
    alerts_placeholder.subheader("Real-Time Alerts")
    alerts_placeholder.empty()

    for _, row in df[df["risk_score"] >= 60].iterrows():
        alerts_placeholder.warning(
            f"⚠ ALERT: Aircraft {row['aircraft_id']} Risk Level {row['risk_score']}"
        )

    # ----------------------------
    # TABLE
    # ----------------------------
    table_placeholder.subheader("Aircraft Monitoring Table")
    table_placeholder.dataframe(
        df[["aircraft_id","speed","altitude","risk_score"]]
    )

    # ----------------------------
    # ANALYTICS
    # ----------------------------
    risk_counts = df["risk_score"].value_counts()
    chart_placeholder.bar_chart(risk_counts)

    scatter_placeholder.scatter_chart(
        df,
        x="speed",
        y="altitude"
    )

    time.sleep(sleep_time)