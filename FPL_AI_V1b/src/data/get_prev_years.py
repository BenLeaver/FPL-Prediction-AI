import pandas as pd
import os

from src.utils.feature_engineering import calc_cards_per_90, calc_pts_per_90

def process_season_data(df):
    """Process a DataFrame of raw player statistics into a cleaner format.

    Filters relevant columns, calculates per-90 metrics (cards and points per 90 minutes),
    and removes unnecessary columns (e.g., raw red/yellow card counts). Rounds all numeric
    values to two decimal places for consistency.

    Args:
        df (pd.DataFrame): Raw player data for a single season.

    Returns:
        pd.DataFrame: Cleaned and processed player data.
    """
    useful_columns = [
        "first_name", "second_name", "element_type", "total_points",
        "goals_scored", "assists", "minutes", "goals_conceded",
        "creativity", "influence", "threat", "bonus", "ict_index",
        "clean_sheets", "red_cards", "yellow_cards"
    ]
    df = df[useful_columns].copy()

    df["cards_per_90"] = df.apply(lambda row: calc_cards_per_90(row["red_cards"] + row["yellow_cards"], row["minutes"]), axis=1)
    df["points_per_90"] = df.apply(lambda row: calc_pts_per_90(row["total_points"], row["minutes"]), axis=1)
    df.drop(columns=["red_cards", "yellow_cards"], inplace=True)
    return df.round(2)


def fetch_and_process_season(year, save_dir="data/prev_years"):
    """
    Fetch, process, and save player stats for a given Premier League season.

    Downloads cleaned player data from the public GitHub FPL dataset, filters
    relevant columns, calculates per-90 stats, and saves to a CSV file.

    Args:
        year (str): The season year in 'YYYY-YY' format (e.g. '2023-24').
        save_dir (str): Directory path to save the processed CSV.
    """
    url = (
        "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/"
        f"master/data/{year}/cleaned_players.csv"
    )
    print(f"Fetching data for {year}...")
    df = pd.read_csv(url)
    df_processed = process_season_data(df)

    os.makedirs(save_dir, exist_ok=True)
    output_path = os.path.join(save_dir, f"{year}_season_data.csv")
    df_processed.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")


def fetch_all_seasons(years, save_dir="data/prev_years"):
    """
    Fetch and process player data for multiple Premier League seasons.

    Iterates over a list of season strings (e.g., '2023-24'), downloads the 
    corresponding data for each, applies processing, and saves to CSV files.

    Args:
        years (list of str): List of season identifiers to process.
        save_dir (str): Directory to save the processed data files.
    """
    for year in years:
        fetch_and_process_season(year, save_dir)


if __name__ == "__main__":
    default_years = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
    fetch_all_seasons(default_years)
