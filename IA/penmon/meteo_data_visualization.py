import pandas as pd
import matplotlib

from penmon.utils import DATASET_FILE

matplotlib.use('agg')

import matplotlib.pyplot as plt

MONTHS = [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"
]

MONTHS_SHORT = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
    "Aug", "Sept", "Oct", "Nov", "Dec"
]


def get_irrigation_for_given_date(df: pd.DataFrame, date: str, selected_column: str) -> float:
    # Return irrigation for given date
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df_plot = df[df["Date"] == date]
    return df_plot[selected_column].values[0]


def generate_df_mean_irrigation_per_month_for_given_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    # Make a graph of the "Irrigation (mm)" column per month for the given year
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df_plot = df[df["Date"].dt.year == year]
    df_plot = df_plot.groupby(df_plot["Date"].dt.month)
    df_plot = df_plot.mean(numeric_only=True)
    return df_plot


def generate_df_irrigation_per_day_for_given_month(df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    # Make a graph of the "Irrigation (mm)" column per day for the given month and year
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df_plot = df[(df["Date"].dt.year == year) & (df["Date"].dt.month == month)]
    df_plot = df_plot.groupby(df_plot["Date"].dt.day)
    df_plot = df_plot.mean(numeric_only=True)
    return df_plot


def plot_year(df_plot: pd.DataFrame, selected_column: str) -> None:
    plt.bar(df_plot.index, df_plot[selected_column])
    plt.xlabel("Month")
    plt.ylabel("Irrigation (mm)")
    plt.title(f"{selected_column} per month")
    plt.xticks(range(1, 13), MONTHS_SHORT)
    plt.ylim(0, 10)


def plot_month(df_plot: pd.DataFrame, month_index: int) -> list:
    plt.plot(df_plot["Optimal Irrigation (mm)"])
    plt.xlabel("Day")
    plt.ylabel("Irrigation (mm)")
    plt.title(f"Optimal Irrigation (mm) per day - {MONTHS[month_index - 1]}")
    plt.xticks(range(1, 32, 5))
    plt.ylim(0, 10)


def generate_meteorological_data_visualization(place: str, date: str) -> dict:
    # Load data/dataset-place.csv file into a dataframe
    df = pd.read_csv(f"{DATASET_FILE}-{place}.csv", sep=",")

    # Extract year and month from date
    year = int(date.split("-")[0])
    month = int(date.split("-")[1])

    # Get index of the previous and next month
    previous_month = month - 1 if month > 1 else 12
    next_month = month + 1 if month < 12 else 1

    months_extract = {
        "previous": previous_month,
        "current": month,
        "next": next_month
    }

    returned_object = {
        "day": {},
        "month": {},
        "year": {}
    }

    # Create new fig with one slot
    df_plot = generate_df_mean_irrigation_per_month_for_given_year(df, year)
    for col in ["Min Irrigation (mm)", "Optimal Irrigation (mm)", "Max Irrigation (mm)"]:
        # Return data for day
        returned_object["day"][col.split(" ")[0].lower()] = get_irrigation_for_given_date(df, date, col)

        # Return fig for year
        fig = plt.figure(figsize=(10, 10))
        plot_year(df_plot, col)
        returned_object["year"][col.split(" ")[0].lower()] = fig

    # Iterate over months_extract
    for key, value in months_extract.items():
        df_plot = generate_df_irrigation_per_day_for_given_month(df, year, value)
        fig = plt.figure(figsize=(10, 10))
        plot_month(df_plot, value)
        returned_object["month"][key] = fig

    # Plot day by display the value of the day
    # plt.tight_layout()

    # Return irrigation for the day, for the month and min, and for year
    return returned_object
