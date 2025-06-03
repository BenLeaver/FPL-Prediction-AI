import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv('training_data/2023-24_training_data.csv')

# Drop the unnamed index column if it exists
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Drop unnecessary columns
df = df.drop(columns=["first_name", "second_name", "year"])

# Map 'element_type' to numeric values
element_type_mapping = {
    "GK": 0,
    "DEF": 1,
    "MID": 2,
    "FWD": 3
}

df["element_type"] = df["element_type"].map(element_type_mapping)

# Identify columns with the 'prev_' prefix
prev_columns = [col for col in df.columns if col.startswith('prev_')]

# Fill missing values in each 'prev_' column with the column mean
for col in prev_columns:
    mean_value = df[col].mean()
    df[col].fillna(mean_value, inplace=True)

df = df.round(2)

df.to_csv('training_data/training_data_cleaned.csv', index=False)

