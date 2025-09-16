## FPL AI V1B

### Overview

This version is a fully refactored and maintainable iteration of the AI, building on V1A. The main goal remains predicting total points for FPL players, but this version introduces several improvements.

**To get the current predictions, use command `python -m scripts.predict_pipeline`. Adjust the gameweek and year in predict_pipeline.py as required.**

### Improvements

- Modular and maintainable pipeline for data collection, preprocessing, and feature engineering.
- Ability to pull **current season data** from the official FPL API.
- **Predownload** raw player data together to reduce network waits — improving training data preparation speed by ~20x.
- Other Data pipeline performance improvements, such as replacing .query with boolean indexing.
- Optimised **Random Forest model hyperparameters** using **grid-search**, **random-search** and **cross-validation**.
- Ability to **print top player predictions by position**, which is easier to see than a csv file.

### Limitations

Some limitations remain or are new compared to V1A:

- Predictions are still based on **total points**, so they are not precise for a **single gameweek** or **short-term forecasts**.
- **Fixture difficulty** and opponent strength are not included in the model.
- **Recent form** or **injuries** are not explicitly factored in, although current season cumulative stats help partially.
- Random Forest model is used; while hyperparameters are tuned, **other model types have not been explored** extensively.
- **Changes to FPL rules** over the years (e.g. bonus points added in 2025–26) may affect consistency of predictions.
- **Players without prior PL data** are harder to predict early in the season.

### Files

#### Training Model

- [`train_pipeline.py`](scripts/train_pipeline.py) – Runs the full training pipeline, including data collection and preprocessing.
- [`get_prev_years.py`](src/data/get_prev_years.py) – Collects data from previous seasons. Adds features like `cards_per_90` and `pts_per_90`.
- [`predownload_seasons.py`](src/data/predownload_seasons.py) – Downloads all gameweek data to speed up later steps.
- [`get_current_year.py`](src/data/get_current_year.py) – Retrieves current season data for players.
- [`prepare_training_data.py`](src/data/prepare_training_data.py) – Combines historical and current data for training.
- [`preprocess_training.py`](src/data/preprocess_training.py) – Cleans and encodes features (drops IDs, encodes element types, fills missing values).
- [`train_random_forest.py`](src/models/train_random_forest.py) – Trains and evaluates the Random Forest model (MSE, R²), then saves it.

#### Predictions

- [`predict_pipeline.py`](scripts/predict_pipeline.py) – Runs the full prediction pipeline, saves outputs, and prints top 10 players by position.
- [`pull_current_fpl_api.py`](src/data/pull_current_fpl_api.py) – Pulls live data from the FPL API and merges with prior season stats.
- [`make_predictions.py`](src/models/make_predictions.py) – Loads the trained model to generate current-season predictions.
- [`get_positional_predictions.py`](src/analysis/get_positional_predictions.py) – Extracts and displays top players by position.
