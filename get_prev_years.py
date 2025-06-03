import pandas as pd

years = ["2020-21", "2021-22", "2022-23", "2023-24"]


def calc_cards_per_90(row):
    """
    Calculate cards per 90 minutes for a player.

    If a player has played less than 270 minutes (3 full matches), 
    the result is set to 0.
    """
    if row["minutes"] < 270:
        return 0
    total_cards = row["red_cards"] + row["yellow_cards"]
    return 90 * total_cards / row["minutes"]


def calc_pts_per_90(row):
    """
    Calculate points per 90 minutes for a player.

    If a player has played less than 270 minutes, the result is set to 0.
    """
    if row["minutes"] < 270:
        return 0
    return 90 * row["total_points"] / row["minutes"]


for year in years:
    url = (
        "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/"
        f"master/data/{year}/cleaned_players.csv"
    )
    df = pd.read_csv(url)

    useful_columns = [
        "first_name", "second_name", "element_type", "total_points",
        "goals_scored", "assists", "minutes", "goals_conceded",
        "creativity", "influence", "threat", "bonus", "ict_index",
        "clean_sheets", "red_cards", "yellow_cards"
    ]
    df = df[useful_columns]

    df["cards_per_90"] = df.apply(calc_cards_per_90, axis=1)
    df["points_per_90"] = df.apply(calc_pts_per_90, axis=1)
    df = df.drop(columns=["red_cards", "yellow_cards"])
    df = df.round(2)

    df.to_csv(f"prev_years_data/{year}_season_data.csv", index=False)
