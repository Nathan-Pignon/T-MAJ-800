import pandas as pd

from penmon.utils import DATASET_FILE, VINEYARDS_FILE, extract_dataset_file, check_dataset_file_exists


def generate_cities_file() -> str:
    # Load data/dataset.csv file into a dataframe
    df = pd.read_csv(f"{DATASET_FILE}.csv", sep=",")

    # Trim columns name
    df.columns = df.columns.str.strip()

    # Delete all columns except "Relevés journaliers"
    df = df.drop(df.columns.difference(["Relevés journaliers"]), axis=1)

    # Rename "Relevés journaliers" column to "name"
    df = df.rename(columns={"Relevés journaliers": "name"})

    # Extract cities names from "name" column's rows
    # Each row in this column are in the following format:
    # https://www.prevision-meteo.ch/climat/journalier/vigite-du-haumet/2021-07
    # Here, we want to get vigite-du-haumet from the string
    df["name"] = df["name"].str.split("/").str[-2]

    # Drop duplicates
    df = df.drop_duplicates(subset=["name"])

    # Remove NaN values
    df = df.dropna()

    # Create columns latitude, altitude and fill them with 0
    df["latitude"] = 0
    df["altitude"] = 0

    # Save dataframe to data/cities.csv
    df.to_csv(f"{VINEYARDS_FILE}.csv", index=False)
    return "Vineyards file created"


def manage_cities_data():
    # Check if dataset file exists
    if not check_dataset_file_exists(DATASET_FILE):
        res = extract_dataset_file(DATASET_FILE)
        if not res:
            return f"Dataset file not found"

    # Check if data/cities.csv exists
    if check_dataset_file_exists(VINEYARDS_FILE):
        return "Vineyards file already exists"

    return generate_cities_file()


def get_cities_list():
    # Check if data/cities.csv exists
    if not check_dataset_file_exists(VINEYARDS_FILE):
        res = manage_cities_data()
        if not res:
            return f"Dataset file not found"

    # Load data/cities.csv file into a dataframe
    df = pd.read_csv(f"{VINEYARDS_FILE}.csv", sep=",")

    # Return list of cities
    return df["name"].tolist()


def get_city_details(name: str):
    # Check if data/cities.csv exists
    if not check_dataset_file_exists(VINEYARDS_FILE):
        res = manage_cities_data()
        if not res:
            return f"Dataset file not found"

    # Load data/cities.csv file into a dataframe
    df = pd.read_csv(f"{VINEYARDS_FILE}.csv", sep=",")

    # Keep only lines containing name in "name" column
    df = df[df["name"].str.contains(name)]

    # If no vineyard found, return None
    if df.empty:
        return None

    # Return vineyard details
    return df.to_dict('records')[0]


def update_city_details(name: str, latitude: float, altitude: int):
    # Check if data/vineyards.csv exists
    if not check_dataset_file_exists(VINEYARDS_FILE):
        return f"Dataset file not found"

    # Load data/vineyards.csv file into a dataframe
    df = pd.read_csv(f"{VINEYARDS_FILE}.csv", sep=",")

    # Check if name is in "name" column
    if not df["name"].str.contains(name).any():
        return f"Vineyard {name} not found"

    # Update line with name in "name" column
    df.loc[df["name"] == name, "latitude"] = latitude
    df.loc[df["name"] == name, "altitude"] = altitude

    # Save dataframe to data/vineyards.csv
    df.to_csv(f"{VINEYARDS_FILE}.csv", index=False)

    return get_city_details(name)
