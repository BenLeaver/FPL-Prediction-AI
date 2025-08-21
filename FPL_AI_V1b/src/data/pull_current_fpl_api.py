import requests
import pandas as pd
import json
from datetime import datetime, timezone
import os
from src.utils.feature_engineering import calc_cards_per_90, calc_pts_per_90, normalize_name

def pull_api_data():
    """Pull the latest data from the official FPL API.
    
    Fetches the player elements dataset from the FPL `bootstrap-static`
    endpoint, saves the raw data to a timestamped CSV in 
    `data/raw/official_fpl_api/`, and returns it as a DataFrame.

    Returns:
        df (pd.DataFrame): The raw FPL player data with the following 
        101 columns including player names and performance statistics:
        
        can_transact,can_select,chance_of_playing_next_round,
        chance_of_playing_this_round,code,cost_change_event,
        cost_change_event_fall,cost_change_start,
        cost_change_start_fall,dreamteam_count,element_type,ep_next,
        ep_this,event_points,first_name,form,id,in_dreamteam,news,
        news_added,now_cost,photo,points_per_game,removed,second_name,
        selected_by_percent,special,squad_number,status,team,team_code,
        total_points,transfers_in,transfers_in_event,transfers_out,
        transfers_out_event,value_form,value_season,web_name,region,
        team_join_date,birth_date,has_temporary_code,opta_code,minutes,
        goals_scored,assists,clean_sheets,goals_conceded,own_goals,
        penalties_saved,penalties_missed,yellow_cards,red_cards,saves,
        bonus,bps,influence,creativity,threat,ict_index,
        clearances_blocks_interceptions,recoveries,tackles,
        defensive_contribution,starts,expected_goals,expected_assists,
        expected_goal_involvements,expected_goals_conceded,
        influence_rank,influence_rank_type,creativity_rank,
        creativity_rank_type,threat_rank,threat_rank_type,
        ict_index_rank,ict_index_rank_type,
        corners_and_indirect_freekicks_order,
        corners_and_indirect_freekicks_text,direct_freekicks_order,
        direct_freekicks_text,penalties_order,penalties_text,
        expected_goals_per_90,saves_per_90,expected_assists_per_90,
        expected_goal_involvements_per_90,
        expected_goals_conceded_per_90,goals_conceded_per_90,
        now_cost_rank,now_cost_rank_type,form_rank,form_rank_type,
        points_per_game_rank,points_per_game_rank_type,selected_rank,
        selected_rank_type,starts_per_90,clean_sheets_per_90,
        defensive_contribution_per_90
    """
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = requests.get(url)
    data = json.loads(response.text)
    df = pd.DataFrame.from_dict(data['elements'])
    now = datetime.now(timezone.utc)
    formatted = now.strftime("%Y_%m_%d_%H_%M_%S")
    path = f'data/raw/official_fpl_api/{formatted}_fpl_api.csv'
    df.to_csv(path, index=False)
    return df

def process_api_data(current_df, year, prev_year, gw):
    """Transform raw FPL API data into a model-ready dataset.

    Args:
        current_df (pd.DataFrame): Current season FPL player data.
        year (str): Current season (e.g., "2025-26").
        prev_year (str): Previous season (e.g., "2024-25").
        gw (int): Gameweek number (the last gw which has been played).

    Returns:
        pd.DataFrame: Processed model-ready dataset including:
            - Player metadata (names, code, element_type, year, gw).
            - Previous season features (prefixed with `prev_`).
            - Current season features (prefixed with `current_`).
            - Engineered metrics (cards_per_90, points_per_90).
            - Missing previous season numeric values filled with column 
            means.
"""
    
    def drop_name_duplicates(df):
        return df[~df.duplicated(subset=["first_name", "second_name"], keep=False)]  
    
    current_df = current_df.copy()
    
    keep_cols_current = [
        "first_name", "second_name", "element_type", "total_points", 
        "goals_scored", "assists", "minutes", "goals_conceded", "creativity", 
        "influence", "threat", "bonus", "ict_index", "clean_sheets", 
        "yellow_cards", "red_cards", "code"
        ]
    current_df = current_df[keep_cols_current]
    
    prev_path = os.path.join("data", "prev_years", f"{prev_year}_season_data.csv")
    prev_df = pd.read_csv(prev_path)
    prev_df = prev_df.copy()
    
    current_df['first_name_norm'] = current_df['first_name'].apply(normalize_name)
    current_df['second_name_norm'] = current_df['second_name'].apply(normalize_name)
    prev_df['first_name_norm'] = prev_df['first_name'].apply(normalize_name)
    prev_df['second_name_norm'] = prev_df['second_name'].apply(normalize_name)
    
    # Drop players with duplicate names.
    current_clean = current_df
    prev_clean = drop_name_duplicates(prev_df)
    
    prev_clean["points_per_90_prev"] = prev_clean["points_per_90"]
    prev_clean["cards_per_90_prev"] = prev_clean["cards_per_90"]
    
    merged = pd.merge(
        current_clean,
        prev_clean,
        left_on=["first_name_norm", "second_name_norm"],
        right_on=["first_name_norm", "second_name_norm"],
        how="left",
        suffixes=("", "_prev")
    )
    merged = merged.drop(columns=['first_name_norm', 'second_name_norm'])
    
    output = pd.DataFrame()
       
    output = pd.DataFrame()
    output["code"] = merged["code"]
    output["first_name"] = merged["first_name"]
    output["second_name"] = merged["second_name"]
    # Element type index is 1 more in current season (2025-26) than in training data
    output["element_type"] = merged["element_type"] - 1
    output["year"] = year
    output["gw"] = gw
    
    # Previous season features (if player was in prev_years, otherwise NaN)
    output["prev_total_points"]   = merged.get("total_points_prev")
    output["prev_goals_scored"]   = merged.get("goals_scored_prev")
    output["prev_assists"]        = merged.get("assists_prev")
    output["prev_minutes"]        = merged.get("minutes_prev")
    output["prev_goals_conceded"] = merged.get("goals_conceded_prev")
    output["prev_creativity"]     = merged.get("creativity_prev")
    output["prev_influence"]      = merged.get("influence_prev")
    output["prev_threat"]         = merged.get("threat_prev")
    output["prev_bonus"]          = merged.get("bonus_prev")
    output["prev_ict_index"]      = merged.get("ict_index_prev")
    output["prev_clean_sheets"]   = merged.get("clean_sheets_prev")
    output["prev_cards_per_90"]   = merged.get("cards_per_90_prev")
    output["prev_points_per_90"]  = merged.get("points_per_90_prev")
    output["prev_season_played"]  = merged["minutes_prev"].notna()
    
    # Current season features
    # TODO: Find out how to get matches for gw and player to tell if it is a double gw.
    # At the moment just assumes it is a single gameweek.
    output["matches"] = 1
    output["current_total_points"]   = merged["total_points"]
    output["current_goals_scored"]   = merged["goals_scored"]
    output["current_assists"]        = merged["assists"]
    output["current_minutes"]        = merged["minutes"]
    output["current_goals_conceded"] = merged["goals_conceded"]
    output["current_creativity"]     = merged["creativity"]
    output["current_influence"]      = merged["influence"]
    output["current_threat"]         = merged["threat"]
    output["current_bonus"]          = merged["bonus"]
    output["current_ict_index"]      = merged["ict_index"]
    output["current_clean_sheets"]   = merged["clean_sheets"]
    
    output["current_cards_per_90"] = merged.apply(
        lambda row: calc_cards_per_90(
            row.get("yellow_cards", 0) + row.get("red_cards", 0),
            row.get("minutes", 0)
        ),
        axis=1
    )
    
    output["current_points_per_90"] = merged.apply(
        lambda row: calc_pts_per_90(
            row.get("total_points"),
            row.get("minutes", 0)
        ),
        axis=1
    )
    
    prev_cols = [col for col in output.columns if col.startswith("prev_")]
    for col in prev_cols:
        if pd.api.types.is_numeric_dtype(output[col]):
            output[col] = output[col].fillna(output[col].mean())
    
    output = output.round(2)  
    
    return output
    
def save_model_ready_api_data(gw, year="2025-26", prev_year="2024-25"):
    """Generate and save model-ready API data for a given gameweek.

    Pulls the latest FPL API data, processes it into the model-ready
    format (with current and previous season features), and saves
    it to `data/pre-predictions/processed_data`.

    Args:
        gw (int): Gameweek number.
        year (str, optional): Current season (default "2025-26").
        prev_year (str, optional): Previous season (default "2024-25").
    """
    df = pull_api_data()
    output_df = process_api_data(df, year, prev_year, gw)
    
    base_dir = "data/pre-predictions/processed_data"
    os.makedirs(base_dir, exist_ok=True)
    filename = f"{gw}_{year}_model_ready.csv"
    file_path = os.path.join(base_dir, filename)
    output_df.to_csv(file_path, index=False)
    print(f"Saved model-ready data for GW{gw} {year} to {file_path}")

save_model_ready_api_data(1)
