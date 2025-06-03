import pandas as pd

def get_current_player_data(year, first_name, second_name):
    """
    Retrieves concurrent player season data for a given player and season.

    For example, if a player has played 90 minutes in GW1 and 90 minutes in 
    GW2, then current_minutes will be 90 for GW1 and 180 for GW2.

    Args:
        year (str): The season from which the data should be taken (e.g. '2021-22').
        first_name (str): The first name of the player.
        second_name (str): The second name of the player.

    Returns:
        pandas.DataFrame: A DataFrame containing concurrent player season data 
        with the following columns:
            - 'gw'
            - 'matches'
            - 'current_total_points'
            - 'current_goals_scored'
            - 'current_assists'
            - 'current_minutes'
            - 'current_goals_conceded'
            - 'current_creativity'
            - 'current_influence'
            - 'current_threat'
            - 'current_bonus'
            - 'current_ict_index'
            - 'current_clean_sheets'
            - 'current_cards'
            - 'current_cards_per_90'
            - 'current_points_per_90'
    """
    
    df = pd.DataFrame(columns=[ 'gw', 'matches',
        'current_total_points', 'current_goals_scored', 'current_assists', 
        'current_minutes', 'current_goals_conceded', 'current_creativity', 
        'current_influence', 'current_threat', 'current_bonus', 
        'current_ict_index', 'current_clean_sheets', 'current_cards', 
        'current_cards_per_90', 'current_points_per_90'])
    
    col_map = {
        'current_total_points': 'total_points',
        'current_goals_scored': 'goals_scored',
        'current_assists': 'assists',
        'current_minutes': 'minutes',
        'current_goals_conceded': 'goals_conceded',
        'current_creativity': 'creativity',
        'current_influence': 'influence',
        'current_threat': 'threat',
        'current_bonus': 'bonus',
        'current_ict_index': 'ict_index',
        'current_clean_sheets': 'clean_sheets'
    }
    prev_gw = None
    for n in range(1, 39):
        
        # Get url for this gw
        url = f'https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{year}/gws/gw{n}.csv'

        # Add current gw data as new row to df
        gw_data = pd.read_csv(url)
        name = f"{first_name} {second_name}"
        player_row = gw_data[gw_data['name'] == name]
        
        if player_row.empty:
            # Player may not exist in the game yet
            print(f"player_row empty for {n} {name}")
        else:
            num_matches = player_row.shape[0]
            new_row = {}
            
            if num_matches == 0:
                # Blank gameweek
                if prev_gw is not None:
                    new_row = prev_gw
            elif num_matches == 1:
                # Normal gameweek
                this_gw = {dest: player_row[src].values[0] for dest, src in col_map.items()}
                this_gw['current_cards'] = player_row['yellow_cards'].values[0] + player_row['red_cards'].values[0]
                
                new_row = this_gw
                if prev_gw is not None:
                    new_row = {key: this_gw.get(key, 0) + prev_gw.get(key, 0) for key in set(this_gw) | set(prev_gw)}
                prev_gw = new_row
                
                if new_row['current_minutes'] < 270:
                    new_row['current_cards_per_90'] = 0
                    new_row['current_points_per_90'] = 0
                else:
                    new_row['current_cards_per_90'] = 90 * new_row['current_cards'] / new_row['current_minutes']
                    new_row['current_points_per_90'] = 90 * new_row['current_total_points'] / new_row['current_minutes']
            elif num_matches == 2:
                # Double gameweek
                
                match1 = {dest: player_row[src].values[0] for dest, src in col_map.items()}
                match1['current_cards'] = player_row['yellow_cards'].values[0] + player_row['red_cards'].values[0]
                
                match2 = {dest: player_row[src].values[1] for dest, src in col_map.items()}
                match2['current_cards'] = player_row['yellow_cards'].values[1] + player_row['red_cards'].values[1]
                
                # Add both matches together
                this_gw = {key: match1.get(key, 0) + match2.get(key, 0) for key in set(match1) | set(match2)}
                
                new_row = this_gw
                if prev_gw is not None:
                    new_row = {key: this_gw.get(key, 0) + prev_gw.get(key, 0) for key in set(this_gw) | set(prev_gw)}
                prev_gw = new_row
                
                if new_row['current_minutes'] < 270:
                    new_row['current_cards_per_90'] = 0
                    new_row['current_points_per_90'] = 0
                else:
                    new_row['current_cards_per_90'] = 90 * new_row['current_cards'] / new_row['current_minutes']
                    new_row['current_points_per_90'] = 90 * new_row['current_total_points'] / new_row['current_minutes']
                    
            new_row['gw'] = n
            new_row['matches'] = num_matches
            df.loc[len(df)] = new_row
    df = df.round(2)
    return df