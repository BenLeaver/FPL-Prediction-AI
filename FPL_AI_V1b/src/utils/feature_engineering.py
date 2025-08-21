import pandas as pd
import unicodedata

def map_element_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Map 'element_type' to numeric values for modelling.

    Mapping:
        GK  -> 0
        DEF -> 1
        MID -> 2
        FWD -> 3

    Args:
        df (pd.DataFrame): Input DataFrame with 'element_type' column.

    Returns:
        pd.DataFrame: DataFrame with numeric 'element_type'.
    """
    mapping = {'GK': 0, 'DEF': 1, 'MID': 2, 'FWD': 3}
    df['element_type'] = df['element_type'].map(mapping)
    return df


def calc_cards_per_90(cards, minutes):
    """
    Calculate cards per 90 minutes, with a 270-minute minimum threshold.
    
    Args:
        cards (int): Total number of red + yellow cards.
        minutes (int): Total minutes played.

    Returns:
        float: Cards per 90 minutes, or 0 if minutes < 270.
    """
    if minutes < 270:
        return 0.0
    return 90 * cards / minutes


def calc_pts_per_90(points, minutes):
    """
    Calculate points per 90 minutes, with a 270-minute minimum threshold.
    
    Args:
        points (int): Total FPL points.
        minutes (int): Total minutes played.

    Returns:
        float: Points per 90 minutes, or 0 if minutes < 270.
    """
    if minutes < 270:
        return 0.0
    return 90 * points / minutes

def get_feature_columns(df: pd.DataFrame, exclude=None) -> list:
    """
    Return a list of feature columns, excluding specified ones.

    Args:
        df (pd.DataFrame): The input DataFrame.
        exclude (list, optional): Columns to exclude.

    Returns:
        list: List of column names to be used as model features.
    """
    if exclude is None:
        exclude = ['first_name', 'second_name', 'year', 'total_points']
    return [col for col in df.columns if col not in exclude]

def normalize_name(name):
    """
    Normalize player names by removing accents and converting to lowercase.
    """
    if pd.isna(name):
        return ""
    return unicodedata.normalize('NFKD', str(name)).encode(
        'ASCII', 'ignore').decode('utf-8').lower().strip()