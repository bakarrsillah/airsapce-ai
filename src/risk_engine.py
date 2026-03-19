import pandas as pd
from data_processor import clean_data, create_features
from anomaly_detector import load_data, prepare_features, train_model, detect_anomalies
from airspace_zones import check_restricted_zone


def calculate_risk(row):

    if row["restricted_zone"] == True:
        return 95

    elif row["anomaly"] == -1:
        return 60

    else:
        return 10


def add_zone_detection(df):

    df["restricted_zone"] = df.apply(
        lambda row: check_restricted_zone(row["latitude"], row["longitude"]),
        axis=1
    )

    return df


def add_risk_scores(df):

    df["risk_score"] = df.apply(calculate_risk, axis=1)

    return df


if __name__ == "__main__":

    df = load_data()

    df = clean_data(df)
    df = create_features(df)

    features = prepare_features(df)

    model = train_model(features)

    df = detect_anomalies(model, features, df)

    df = add_zone_detection(df)

    df = add_risk_scores(df)

    print(df[[
        "aircraft_id",
        "speed",
        "altitude",
        "anomaly",
        "restricted_zone",
        "risk_score"
    ]])