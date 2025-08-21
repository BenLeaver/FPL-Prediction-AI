import os
import pandas as pd
import joblib

def load_model(model_path: str):
    """Load a trained model given a path."""
    return joblib.load(model_path)

def load_current_data(input_path: str) -> pd.DataFrame:
    """Load the pre-processed current season data."""
    return pd.read_csv(input_path)

def prepare_features(df: pd.DataFrame, drop_cols=None):
    """
    Prepare features for prediction by removing non-feature columns.
    Returns the features and the dropped columns separately so they can
    be added back later.
    """
    if drop_cols is None:
        drop_cols = ["code", "first_name", "second_name", "year"]

    meta_df = df[drop_cols].copy()
    X = df.drop(columns=drop_cols, errors="ignore")
    return X, meta_df

def add_predictions(X: pd.DataFrame, predictions, meta_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add predictions, restore meta columns, reorder, and sort by prediction.
    """
    df_out = X.copy()
    df_out["total_points_predictions"] = predictions
    df_out = pd.concat([meta_df.reset_index(drop=True), df_out.reset_index(drop=True)], axis=1)
    
    cols = ["total_points_predictions"] + [c for c in df_out.columns if c != "total_points_predictions"]
    df_out = df_out[cols]
    
    df_out = df_out.sort_values(by="total_points_predictions", ascending=False).reset_index(drop=True)
    
    df_out = df_out.round(2)
    return df_out


def save_predictions(df: pd.DataFrame, output_path: str):
    """Save predictions dataframe to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)


def run_prediction_pipeline(
    model_path: str,
    input_data_path: str,
    output_path: str
):
    """Full pipeline to load data, predict, and save results.
    """
    print(f"Loading model from {model_path}...")
    model = load_model(model_path)

    print(f"Loading current season data from {input_data_path}...")
    current_df = load_current_data(input_data_path)

    print("Preparing features...")
    X, meta_df = prepare_features(current_df)

    print("Making predictions...")
    preds = model.predict(X)

    print("Adding predictions to dataframe...")
    final_df = add_predictions(X, preds, meta_df)

    print(f"Saving predictions to {output_path}...")
    save_predictions(final_df, output_path)
    print("Done.")
    
    return final_df


if __name__ == "__main__":
    model_path = "models/random_forest_model.pkl"
    input_data_path = "data/pre-predictions/processed_data/1_2025-26_model_ready.csv"
    output_path = "outputs/predictions/1_2025-26_v1b_predictions.csv"

    run_prediction_pipeline(model_path, input_data_path, output_path)