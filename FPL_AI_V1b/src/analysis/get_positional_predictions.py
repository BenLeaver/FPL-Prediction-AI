import pandas as pd
import os

ELEMENT_TYPE_MAP = {0: "Goalkeepers", 1: "Defenders", 2: "Midfielders", 3: "Forwards"}


def get_top_n(df: pd.DataFrame, element_type: int, n: int) -> pd.DataFrame:
    """
    Get the top N players by predicted total points for a given element type.

    This function filters the prediction DataFrame by the specified
    `element_type` (e.g., 0 = GK, 1 = DEF, 2 = MID, 3 = FWD depending on
    your encoding), sorts the players in descending order of their
    predicted total points, and returns the top N players.

    Args:
        df (pd.DataFrame): DataFrame containing player predictions.
            Must include columns:
                - "element_type"
                - "total_points_predictions"
        element_type (int): The player element type to filter on.
        n (int): The number of top players to return.

    Returns:
        pd.DataFrame: A DataFrame containing the top N players of the
        specified element type, sorted by predicted total points
        (highest first).
    """
    filtered = df[df["element_type"] == element_type]
    top_n = filtered.sort_values(by="total_points_predictions", ascending=False).head(n)
    return top_n.reset_index(drop=True)


def show_top_players_by_position(df: pd.DataFrame, n: int = 10) -> None:
    """
    Display the top N players for each element type (position) based on predicted total points.

    Args:
        df (pd.DataFrame): DataFrame containing player predictions.
            Must include columns:
                - "element_type"
                - "first_name"
                - "second_name"
                - "total_points_predictions"
        n (int, optional): Number of top players to display per position. Defaults to 10.
    """

    for element_type, position_name in ELEMENT_TYPE_MAP.items():
        print(f"\n=== Top {n} {position_name} ===")
        top_n = get_top_n(df, element_type, n)

        for rank, row in top_n.iterrows():
            full_name = f"{row['first_name']} {row['second_name']}"
            predicted_points = row["total_points_predictions"]
            print(f"{rank+1}. {full_name:<25} {predicted_points:.2f} pts")


def load_final_predictions(gw: int, year: str) -> pd.DataFrame:
    """
    Load the final predictions DataFrame for a given gameweek and season.

    Args:
        gw (int): The gameweek number.
        year (str): The season string (e.g., "2025-26").

    Returns:
        pd.DataFrame: The predictions DataFrame.

    Raises:
        FileNotFoundError: If the predictions file does not exist.
    """
    file_path = os.path.join(
        "outputs", "predictions", f"{gw}_{year}_v1b_predictions.csv"
    )

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Predictions file not found: {file_path}")

    return pd.read_csv(file_path)


if __name__ == "__main__":
    print("main")
    final_df = load_final_predictions(1, "2025-26")
    print("<==== Top 10 Predictions after GW3 ====>")
    show_top_players_by_position(final_df, 20)
