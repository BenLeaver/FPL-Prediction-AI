import pandas as pd
import joblib

ELEMENT_TYPE_MAPPING = {
    'GK': 0,
    'DEF': 1,
    'MID': 2,
    'FWD': 3
}

def predict_total_points(input_csv, output_csv):
    """Creates an output csv containing the predictions for each 
    player and gameweek in the input csv.

    Args:
        input_csv (str): Path of the csv to be used as input data. Must 
            have the following columns:
            - first_name
            - second_name
            - element_type
            - year
            - prev_total_points
            - prev_goals_scored
            - prev_assists
            - prev_minutes
            - prev_goals_conceded
            - prev_creativity
            - prev_influence
            - prev_threat
            - prev_bonus
            - prev_ict_index
            - prev_clean_sheets
            - prev_cards_per_90
            - prev_points_per_90
            - prev_season_played
            - gw
            - matches
            - current_total_points
            - current_goals_scored
            - current_assists
            - current_minutes
            - current_goals_conceded
            - current_creativity
            - current_influence
            - current_threat
            - current_bonus
            - current_ict_index
            - current_clean_sheets
            - current_cards_per_90
            - current_points_per_90
            - total_points (optional)
        output_csv (str): Path of the output csv file. Has the 
            following columns:
            - first_name
            - second_name
            - year
            - gw
            - actual_total_points (optional)
            - predicted_total_points
        
    """
    df = pd.read_csv(input_csv)
    preserved_columns = df[['first_name', 'second_name', 'year']]
    df['element_type'] = df['element_type'].map(ELEMENT_TYPE_MAPPING)
    df_model_input = df.drop(['first_name', 'second_name', 'year'], axis=1)
    if 'total_points' in df.columns:
        df_model_input = df_model_input.drop('total_points', axis=1)

    model = joblib.load('models/random_forest_model_v1.pkl')
    predicted_total_points = model.predict(df_model_input)

    output_df = preserved_columns.copy()
    output_df['element_type'] = df['element_type']
    output_df['gw'] = df['gw']
    if 'total_points' in df.columns:
        output_df['actual_total_points'] = df['total_points']
    output_df['predicted_total_points'] = predicted_total_points
    output_df = output_df.sort_values(by='predicted_total_points', ascending=False)
    output_df.to_csv(output_csv, index=False)
    print(f"Predictions saved to {output_csv}")
    
predict_total_points('training_data/2021-22_training_data.csv', '2021-22_predictions.csv')
predict_total_points('training_data/2022-23_training_data.csv', '2022-23_predictions.csv')