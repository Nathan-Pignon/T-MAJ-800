import pandas as pd
import matplotlib.pyplot as plt

MONTHS = [
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"
]

MONTHS_SHORT = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
    "Aug", "Sept", "Oct", "Nov", "Dec"
]

# Dataset file path
DATASET_FILE = "data/dataset"

def generate_df_mean_irrigation_per_month_for_given_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    # Make a graph of the "Irrigiation (mm)" column per month for the given year
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df_plot = df[df["Date"].dt.year == year]
    df_plot = df_plot.groupby(df_plot["Date"].dt.month)
    df_plot = df_plot.mean(numeric_only=True)
    return df_plot
    
    
def generate_df_irrigation_per_day_for_given_month(df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    # Make a graph of the "Irrigiation (mm)" column per day for the given month and year
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df_plot = df[(df["Date"].dt.year == year) & (df["Date"].dt.month == month)]
    df_plot = df_plot.groupby(df_plot["Date"].dt.day)
    df_plot = df_plot.mean(numeric_only=True)
    return df_plot


def plot_year(axis: plt.Axes, df_plot: pd.DataFrame, selected_column: str) -> None:
    axis.bar(df_plot.index, df_plot[selected_column])
    axis.set_xlabel("Month")
    axis.set_ylabel("Irrigation (mm)")
    axis.set_title(f"{selected_column} per month")
    axis.set_xticks(range(1, 13))
    axis.set_xticklabels(MONTHS_SHORT)
    axis.set_ylim(0, 6)


def plot_month(axis: plt.Axes, df_plot: pd.DataFrame, month_index: int) -> None:
    axis.plot(df_plot["Optimal Irrigation (mm)"])
    axis.set_xlabel("Day")
    axis.set_ylabel("Irrigation (mm)")
    axis.set_title(f"Optimal Irrigation (mm) per day - {MONTHS[month_index - 1]}")
    axis.set_ylim(0, 6)


def generate_data_visualization(place: str) -> None:
    # Load data/dataset-place.csv file into a dataframe
    df = pd.read_csv(f"{DATASET_FILE}-{place}.csv", sep=",")

    months_extract = [3, 7, 10]
    years_extract = [2015, 2017, 2020]

    for idx, year in enumerate(years_extract):
        fig, axs = plt.subplots(2, 3, figsize=(10, 8))
        # Title of the figure
        fig.suptitle(f"{place.upper()} - {year}")

        df_plot = generate_df_mean_irrigation_per_month_for_given_year(df, year)
        plot_year(axs[0, 0], df_plot, "Min Irrigation (mm)")
        plot_year(axs[0, 1], df_plot, "Optimal Irrigation (mm)")
        plot_year(axs[0, 2], df_plot, "Max Irrigation (mm)")

        for idx, month in enumerate(months_extract):
            df_plot = generate_df_irrigation_per_day_for_given_month(df, year, month)
            plot_month(axs[1, idx], df_plot, month)

        plt.tight_layout()

        plt.show()
