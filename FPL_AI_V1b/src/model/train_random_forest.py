import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV
import joblib

INPUT_DIR = "data/model_ready"
MODEL_PATH = "models/random_forest_model.pkl"

def load_model_ready_data():
    """
    Load and combine all preprocessed training CSV files.

    Returns:
        pd.DataFrame
            A concatenated DataFrame containing all model-ready 
            training data.
    """
    dfs = []
    for file in os.listdir(INPUT_DIR):
        if file.endswith("_model_ready.csv"):
            path = os.path.join(INPUT_DIR, file)
            df = pd.read_csv(path)
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def train_random_forest():
    """
    Train, evaluate, and save a Random Forest regression model.

    Steps:
    1. Loads training data via `load_model_ready_data()`.
    2. Splits into train/test sets.
    3. Trains a Random Forest model and evaluates performance on test data
       (MSE and R² are printed to console).
    4. Retrains the model on the full dataset using the same hyperparameters.
    5. Saves the trained model as a `.pkl` file for later use.
    """
    df = load_model_ready_data()

    X = df.drop(columns=["total_points"])
    y = df["total_points"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        random_state=42, 
        n_jobs=-1,
        n_estimators=1000,
        max_depth=None,
        max_features='log2',
        min_samples_leaf=1,
        min_samples_split=2
    )
    
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R² Score: {r2:.3f}")
    
    final_model = RandomForestRegressor(
        random_state=42,
        n_jobs=-1,
        n_estimators=1000,
        max_depth=None,
        max_features="log2",
        min_samples_leaf=1,
        min_samples_split=2,
    )
    final_model.fit(X, y)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(final_model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_random_forest()