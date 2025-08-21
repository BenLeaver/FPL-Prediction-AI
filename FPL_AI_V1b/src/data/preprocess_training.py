import pandas as pd
from pathlib import Path
from src.utils.feature_engineering import map_element_type

def preprocess_training_data(processed_dir="data/processed", output_dir="data/model_ready"):
    """
    Preprocess all training data CSVs from processed_dir and save cleaned versions to output_dir.
    Steps:
        1. Drop identifying columns
        2. Map 'element_type' to numeric values
        3. Fill missing 'prev_' columns with column mean
        4. Round numeric columns to 2 decimal places
    """
    processed_path = Path(processed_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    cols_to_drop = ["first_name", "second_name", "year"]

    for csv_file in processed_path.glob("*_training_data.csv"):
        print(f"Processing {csv_file.name}...")

        df = pd.read_csv(csv_file)

        df.drop(columns=cols_to_drop, errors="ignore", inplace=True)

        if "element_type" in df.columns:
            df = map_element_type(df)

        prev_columns = [col for col in df.columns if col.startswith("prev_")]
        for col in prev_columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())

        df = df.round(2)

        output_file = output_path / csv_file.name.replace("_training_data", "_model_ready")
        df.to_csv(output_file, index=False)
        print(f"Saved cleaned data to {output_file}")

if __name__ == "__main__":
    preprocess_training_data()