import pandas as pd
from sklearn.ensemble import IsolationForest
from data_processor import clean_data, create_features


def load_data():

    df = pd.read_csv("data/aircraft_simulation.csv")

    return df


def prepare_features(df):

    features = df[[
        "speed",
        "altitude",
        "speed_change",
        "altitude_change",
        "heading_change"
    ]]

    features = features.fillna(0)

    return features


def train_model(features):

    model = IsolationForest(contamination=0.1)

    model.fit(features)

    return model


def detect_anomalies(model, features, df):

    df["anomaly"] = model.predict(features)

    return df


if __name__ == "__main__":

    df = load_data()

    df = clean_data(df)
    df = create_features(df)

    features = prepare_features(df)

    model = train_model(features)

    df = detect_anomalies(model, features, df)

    print(df[["aircraft_id", "speed", "altitude", "anomaly"]])