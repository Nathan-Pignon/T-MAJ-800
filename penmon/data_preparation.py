import zipfile
import os

import pandas as pd
import lib.penmon as pm


# Crop coefficient per month for vineyard (in order: min, mean, max)
KC = {
    1: [0.2, 0.25, 0.3],
    2: [0.2, 0.25, 0.3],
    3: [0.5, 0.55, 0.7],
    4: [0.5, 0.6, 0.7],
    5: [0.8, 0.9, 1.0],
    6: [0.8, 0.9, 1.2],
    7: [0.9, 1.1, 1.2],
    8: [0.9, 0.95, 1.2],
    9: [0.6, 0.7, 0.9],
    10: [0.3, 0.5, 0.6],
    11: [0.2, 0.25, 0.3],
    12: [0.2, 0.25, 0.3]
}

# Dataset file path
DATASET_FILE = "data/dataset"


def compute_solar_radiation_with_sunshine_minutes(sunshine_minutes: int) -> float:
    return sunshine_minutes * 0.012


def format_sunshine(sunshine: list) -> int:
    if len(sunshine) == 2:
        return int(sunshine[0]) * 60 + int(sunshine[1][:-3])
    return int(sunshine[0]) * 60


def extract_dataset_file() -> bool:
    # Unzip data/dataset.zip file
    try:
        with zipfile.ZipFile(f"{DATASET_FILE}.zip", "r") as zip_ref:
            zip_ref.extractall("data")
        # Rename data/france_meteo_2014tojuillet2021.csv to data/dataset.csv
        os.rename("data/france_meteo_2014tojuillet2021.csv", f"{DATASET_FILE}.csv")

        return True
    except FileNotFoundError:
        return False


def check_dataset_file_exists() -> bool:
    try:
        open(f"{DATASET_FILE}.csv")
        return True
    except FileNotFoundError:
        return extract_dataset_file()


def check_dataset_place_file_exists(place: str) -> bool:
    try:
        open(f"{DATASET_FILE}-{place}.csv")
        return True
    except FileNotFoundError:
        return False


def set_dataframe(place: str) -> pd.DataFrame:
    # Load data/dataset.csv file into a dataframe
    df = pd.read_csv(f"{DATASET_FILE}.csv", sep=",")

    # Trim columns name
    df.columns = df.columns.str.strip()

    # Keep only lines containing place name in "Relevés journaliers" column
    df = df[df["Relevés journaliers"].str.contains(place)]

    # Combine "Description" and "Date" to create a new column "Date"
    # It consists of taking the last 7 characters of "Description" and adding it to the last 2 characters of "Date"
    df["Date"] = df["Date"].str[-2:] + '.' + df["Description"].str[-7:]
    df["Date"].replace(".", "-", regex=True)

    # Reformating "Date" column to be in the format "YYYY-MM-DD" string
    df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y")

    # Manage "Ensoleillement h" column values to combine h and min
    # The values are in the following format "Xh Ymin"
    # We want to compute the column to be X + Y at the end
    df["Ensoleillement h"] = df["Ensoleillement h"].str.split("h")
    df["Ensoleillement h"] = df["Ensoleillement h"].apply(lambda x: format_sunshine(x))

    # Drop "Relevés journaliers" and "Description" columns
    df = df.drop(columns=["Relevés journaliers", "Description"])

    # Create new columns "ETo (en mm)", "Mean Crop Coefficient (KC)", "Min Crop Coefficient (KCmax)",
    # "Max Crop Coefficient (KCmax)", "Min Irrigation (mm)", "Optimal Irrigation (mm)", "Max Irrigation (mm)"
    # and fill them with 0
    df["ETo (en mm)"] = 0
    df["Min Crop Coefficient (KCmax)"] = 0
    df["Max Crop Coefficient (KCmax)"] = 0
    df["Mean Crop Coefficient (KC)"] = 0
    df["Min Irrigation (mm)"] = 0
    df["Optimal Irrigation (mm)"] = 0
    df["Max Irrigation (mm)"] = 0

    return df


def compute_save_data(place: str, station_latitude: float, station_altitude: int, df: pd.DataFrame) -> str:
    # Create a station class with known location and elevation
    station = pm.Station(latitude=station_latitude, altitude=station_altitude)
    station.anemometer_height = 5

    for index, row in df.iterrows():
        try:
            # Getting a day instance
            date = row["Date"].strftime("%Y-%m-%d")
            day = station.day_entry(
                date,
                temp_min=row["Temp min C°"],
                temp_max=row["Temp max C°"],
                wind_speed=row["Vent moyen km/h"],
                radiation_s=compute_solar_radiation_with_sunshine_minutes(row["Ensoleillement h"])
            )

            # Get month index from date
            month = row["Date"].month
            row["ETo (en mm)"] = day.eto()
            row["Min Crop Coefficient (KCmax)"] = KC[month][0]
            row["Mean Crop Coefficient (KC)"] = KC[month][1]
            row["Max Crop Coefficient (KCmax)"] = KC[month][2]
            row["Min Irrigation (mm)"] = day.eto() * KC[month][0]
            row["Optimal Irrigation (mm)"] = day.eto() * KC[month][1]
            row["Max Irrigation (mm)"] = day.eto() * KC[month][2]

            # Update dataframe row
            df.loc[index] = row

        except Exception as e:
            continue

    # Save dataframe to csv file
    df.to_csv(f"{DATASET_FILE}-{place}.csv", index=False)
    return "Dataframe saved"


def prepare_data(place: str, station_latitude: float, station_altitude: int, overwrite_generated_data: bool = False) -> str:
    if not overwrite_generated_data and check_dataset_place_file_exists(place):
        return f"Dataset file for {place} already exists"

    # Check if dataset file exists
    if not check_dataset_file_exists():
        return "Main dataset file not found"

    df: pd.DataFrame = set_dataframe(place)
    return compute_save_data(place, station_latitude, station_altitude, df)
