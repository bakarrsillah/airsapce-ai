import pandas as pd
def load_aircraft_data():

    df = pd.read_csv("data/aircraft_simulation.csv")

    return df
def clean_data(df):

    # remove duplicate aircraft records
    df = df.drop_duplicates()

    # remove missing values
    df = df.dropna()

    # convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df
def create_features(df):

    # speed changes
    df["speed_change"] = df["speed"].diff()

    # altitude changes
    df["altitude_change"] = df["altitude"].diff()

    # heading changes
    df["heading_change"] = df["heading"].diff()

    return df
if __name__ == "__main__":

    df = load_aircraft_data()

    df = clean_data(df)

    df = create_features(df)

    print(df.head())