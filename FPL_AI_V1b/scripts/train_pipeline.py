from src.data.get_prev_years import fetch_all_seasons
from src.data.predownload_seasons import predownload_all
from src.data.prepare_training_data import prepare_training_data
from src.data.preprocess_training import preprocess_training_data
from src.model.train_random_forest import train_random_forest

def run_training_pipeline(years):
    """Run the complete training pipeline for the FPL model.

    The pipeline consists of the following steps:
        1. Fetch historical season data from external sources.
        2. Pre-download all required datasets.
        3. Prepare training datasets for the specified seasons.
        4. Preprocess the datasets into model-ready format.
        5. Train a Random Forest model on the processed data.

    Args:
        years (list of str): List of seasons (e.g., ["2020-21", "2021-22"]) 
            to include in the training pipeline."""
    print("=== Training pipeline started. ===")
    fetch_all_seasons(years)
    predownload_all()
    prepare_training_data(years)
    preprocess_training_data()
    train_random_forest()
    print("=== Training pipeline finished! ===")

if __name__ == "__main__":
    years = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
    run_training_pipeline(years)
