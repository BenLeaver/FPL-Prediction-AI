import os
import pandas as pd

from src.data.pull_current_fpl_api import save_model_ready_api_data
from src.model.make_predictions import run_prediction_pipeline
from src.analysis.get_positional_predictions import show_top_players_by_position


def run_current_predictions(
    gw, year, prev_year, model_path="models/random_forest_model.pkl"
):
    """
    Run the current season prediction pipeline:
      1. Collect current API data and prepare it.
      2. Run the prediction model.
      3. Show top players by position.

    Args:
        gw (int): Gameweek number.
        year (str): Current season, e.g. "2025-26".
        prev_year (str): Previous season, e.g. "2024-25".
        model_path (str): Path to the trained model pickle file.
    """
    input_data_path = f"data/pre-predictions/processed_data/{gw}_{year}_model_ready.csv"
    output_path = f"outputs/predictions/{gw}_{year}_v1b_predictions.csv"

    save_model_ready_api_data(gw, year, prev_year)
    final_df = run_prediction_pipeline(model_path, input_data_path, output_path)
    show_top_players_by_position(final_df)


if __name__ == "__main__":
    run_current_predictions(4, "2025-26", "2024-25")
