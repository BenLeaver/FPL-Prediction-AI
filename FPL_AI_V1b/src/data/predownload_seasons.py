import os
import pandas as pd

SEASONS = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
BASE_DIR = "data/raw"

def download_gw(year, gw):
    """
    Downloads and saves a single gameweek CSV for a given season year.

    Args:
        year (str): Season year (e.g., '2020-21')
        gw (int): Gameweek number (1-38)
    """
    season_dir = os.path.join(BASE_DIR, year)
    os.makedirs(season_dir, exist_ok=True)

    local_path = os.path.join(season_dir, f"gw{gw}.csv")
    if os.path.exists(local_path):
        print(f"Already exists: {local_path}")
        return

    url = f"https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{year}/gws/gw{gw}.csv"
    try:
        df = pd.read_csv(url)
        df.to_csv(local_path, index=False)
        print(f"Downloaded: {local_path}")
    except Exception as e:
        print(f"Error downloading {year} GW{gw}: {e}")

def predownload_all():
    """Downloads all gameweek CSVs for all defined seasons."""
    for season in SEASONS:
        print(f"\n=== Downloading season {season} ===")
        for gw in range(1, 39):
            download_gw(season, gw)

if __name__ == "__main__":
    predownload_all()
