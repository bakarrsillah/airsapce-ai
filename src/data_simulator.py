import pandas as pd
import numpy as np
from datetime import datetime


def simulate_aircraft(num_aircraft=20):

    aircraft_data = []

    for i in range(num_aircraft):

        aircraft = {
            "aircraft_id": f"A{i+1}",
            "latitude": np.random.uniform(8.3, 8.6),
            "longitude": np.random.uniform(-13.3, -13.0),
            "altitude": np.random.randint(5000, 35000),
            "speed": np.random.randint(200, 600),
            "heading": np.random.randint(0, 360),
            "timestamp": datetime.now()
        }

        aircraft_data.append(aircraft)

    df = pd.DataFrame(aircraft_data)

    return df


if __name__ == "__main__":

    df = simulate_aircraft()

    df.to_csv("data/aircraft_simulation.csv", index=False)

    print("Aircraft simulation data saved successfully.")