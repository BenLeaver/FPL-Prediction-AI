import pandas as pd
import get_current_year as gcy

years = ["2020-21", "2021-22", "2022-23", "2023-24"]

# Initialize an empty DataFrame for training data
df = pd.DataFrame(columns=[
    'first_name', 'second_name', 'element_type', 'year', 'prev_total_points',
    'prev_goals_scored', 'prev_assists', 'prev_minutes', 'prev_goals_conceded',
    'prev_creativity', 'prev_influence', 'prev_threat', 'prev_bonus',
    'prev_ict_index', 'prev_clean_sheets', 'prev_cards_per_90', 
    'prev_points_per_90', 'prev_season_played', 'gw', 'matches', 'current_total_points',
    'current_goals_scored', 'current_assists', 'current_minutes', 
    'current_goals_conceded', 'current_creativity', 'current_influence',
    'current_threat', 'current_bonus', 'current_ict_index', 
    'current_clean_sheets', 'current_cards_per_90', 'current_points_per_90',
    'total_points'
    ])



for i in range(2, 3):
    this_year = years[i]
    prev_year = years[i-1]
    
    current_df = pd.read_csv(f'prev_years_data/{this_year}_season_data.csv')
    prev_df = pd.read_csv(f'prev_years_data/{prev_year}_season_data.csv')
    
    for row in current_df.itertuples():
        # Get Previous Season's Stats
        prev_row = prev_df.query('first_name == @row.first_name & second_name == @row.second_name')
        
        # Get Current Season's stats (only used for checking player has unique name)
        current_row = current_df.query('first_name == @row.first_name & second_name == @row.second_name')
        
        if len(prev_row) > 1 or len(current_row) > 1:
            # Multiple players found with the same name
            print(f"Multiple players found with the name {row.first_name} {row.second_name}")
        else:
            # Remove unnecessary data from previous season.
            prev_row = prev_row.drop(columns=['first_name', 'second_name', 'element_type'])
            prev_row = prev_row.reset_index(drop=True)
            
            current_season_player_stats = gcy.get_current_player_data(this_year, row.first_name, row.second_name)
            for gw in range(1, 39):     
                new_row = pd.DataFrame({
                    'first_name': row.first_name,
                    'second_name': row.second_name,
                    'element_type': row.element_type,
                    'year': this_year,
                    'total_points': row.total_points,
                    'gw': gw}, index=[0])
                
                
                if len(prev_row) == 0:
                    # Player not found in previous season.
                    new_row['prev_season_played'] = False
                elif len(prev_row) == 1:
                    # Player data for previous season found.
                    
                    # Add prefix of prev_ to previous season's columns.
                    for column in prev_row.columns:
                        col_text = f"prev_{column}"
                        new_row[col_text] = prev_row[column].values[0]
                    
                    new_row['prev_season_played'] = True
                
                current_gw = current_season_player_stats[current_season_player_stats['gw'] == gw]
                current_gw = current_gw.drop(columns=['gw','current_cards'])
                
                # Check if player exists yet (some players are only added to fpl in later gameweeks)
                if not current_gw.empty:
                    
                    new_row = new_row.reset_index(drop=True)
                    current_gw = current_gw.reset_index(drop=True)
                    new_row = pd.concat([new_row, current_gw], axis=1)        
                    df = pd.concat([df, new_row], ignore_index=True, axis=0)
                    print(f"Training data row successfully added for {gw}, {row.first_name}, {row.second_name}!")
        df.to_csv(f'training_data/{this_year}_training_data.csv', index=False)
    print(f"Year {this_year} finished!")
    
