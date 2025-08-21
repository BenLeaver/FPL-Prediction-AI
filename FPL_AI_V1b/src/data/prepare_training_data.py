import pandas as pd
import os
import time
from src.data.get_current_year import get_current_player_data

def load_season_data(years, i, data_dir="data/prev_years"):
    """
    Load the current and previous season's data for the specified index in the years list.

    Args:
        years (list): List of season strings (e.g., ['2020-21', '2021-22']).
        i (int): Index of the current year in the years list.
        data_dir (str): Path to the directory containing season data CSV files.

    Returns:
        tuple: (this_year (str), prev_df (DataFrame), current_df (DataFrame))
    """
    this_year = years[i]
    prev_year = years[i - 1]

    current_df = pd.read_csv(os.path.join(data_dir, f"{this_year}_season_data.csv"))
    prev_df = pd.read_csv(os.path.join(data_dir, f"{prev_year}_season_data.csv"))

    return this_year, prev_df, current_df

def create_training_row(row, prev_df, current_df, this_year):
    """
    Create a list of training data rows for a player for all gameweeks in the current season.

    Args:
        row (namedtuple): Row object from the current season DataFrame.
        prev_df (DataFrame): DataFrame containing previous season's stats.
        current_df (DataFrame): DataFrame containing current season's stats.
        this_year (str): Current season string (e.g., '2022-23').

    Returns:
        list: List of DataFrames, each representing one row of training data for a gameweek.
    """
    prev_row = prev_df[(prev_df["first_name"] == row.first_name) & (prev_df["second_name"] == row.second_name)]
    current_row = current_df[(current_df["first_name"] == row.first_name) & (current_df["second_name"] == row.second_name)]

    if len(prev_row) > 1 or len(current_row) > 1:
        print(f"Multiple players found with the name {row.first_name} {row.second_name}")
        return []

    prev_row = prev_row.drop(columns=["first_name", "second_name", "element_type"], errors="ignore").reset_index(drop=True)
    current_season_data = get_current_player_data(this_year, row.first_name, row.second_name)

    training_rows = []

    for gw in range(1, 39):
        new_row = pd.DataFrame({
            "first_name": row.first_name,
            "second_name": row.second_name,
            "element_type": row.element_type,
            "year": this_year,
            "total_points": row.total_points,
            "gw": gw
        }, index=[0])

        if len(prev_row) == 0:
            new_row["prev_season_played"] = False
        else:
            for column in prev_row.columns:
                new_row[f"prev_{column}"] = prev_row[column].values[0]
            new_row["prev_season_played"] = True

        current_gw = current_season_data[current_season_data["gw"] == gw].drop(columns=["gw", "current_cards"], errors="ignore")

        if not current_gw.empty:
            new_row = new_row.reset_index(drop=True)
            current_gw = current_gw.reset_index(drop=True)
            training_rows.append(pd.concat([new_row, current_gw], axis=1))

    return training_rows

def prepare_training_data(years, output_dir="data/processed", data_dir="data/prev_years"):
    """
    Generate training data for all seasons by combining previous and current season stats.

    Args:
        years (list): List of season strings in chronological order.
        output_dir (str): Directory to save the output training data CSVs.
        data_dir (str): Directory containing the input season data CSVs.
    """
    os.makedirs(output_dir, exist_ok=True)

    for i in range(1, len(years)):
        this_year, prev_df, current_df = load_season_data(years, i, data_dir)
        df_all = []

        for row in current_df.itertuples():
            rows = create_training_row(row, prev_df, current_df, this_year)
            df_all.extend(rows)

        if df_all:
            full_df = pd.concat(df_all, ignore_index=True)
            output_path = os.path.join(output_dir, f"{this_year}_training_data.csv")
            full_df.to_csv(output_path, index=False)
            print(f"Saved training data for {this_year} to {output_path}")
        else:
            print(f"No valid training data found for {this_year}")

if __name__ == "__main__":
    start = time.time()
    seasons = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
    prepare_training_data(seasons)
    print("Done in", time.time() - start, "seconds")
