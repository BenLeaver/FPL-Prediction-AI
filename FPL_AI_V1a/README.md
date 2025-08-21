## FPL AI V1A


### Overview
This version of the AI was intended to be a very basic prototype, to be used as a base for building future more complex versions of the AI. A random forest regressor model was used, which takes player data for a specific gameweek as input to try and predict how many total points the player will score by the end of the season. The idea is that the best players are those with the highest total points predictions. 

The input data is comprised of:
1. Data from the previous season for that player (if it exists).
2. Data from previous gameweeks in the current season e.g. the number of goals scored so far.
### Limitations
Below are some of the main limitations of this version of the AI for predicting which players are the best picks in FPL:
- Predictions are based on total points so are not as useful for predicting how many points a player will get in a given gameweek, or across the next few gameweeks.
- Predictions don't take into account the next fixtures and the strength of opponent teams.
- Predictions don't take into account a player's recent form.
- Data collection (`prepare_training_data.py`) takes quite a while i.e. about 30 mins per year (>20000 data rows) on my laptop.
- I have not experimented with finding the most optimal model and hyperparameters.
- A significant amount of players have not played at all in the premier league in the previous season, so I have dealt with this missing data by just taking the mean values across players who did play.
### Files
`get_prev_years.py` - Collects data from previous seasons (e.g. https://github.com/vaastav/Fantasy-Premier-League/blob/master/data/2020-21/cleaned_players.csv). Keeps the useful columns and creates two new features `cards_per_90` (instead of red_cards and yellow_cards) and `pts_per_90`.

`get_current_year.py` - Used to retrieve concurrent player season data for a given player and season.

`prepare_training_data.py` - Used to actually put together training data. This includes:
- Player information (name, element_type e.g. MID)
- Gameweek number and year
- Final total points of the player this season
- Previous season's data
- Current season's concurrent data up until the previous gameweek

`preprocess_training.py` - Removes columns `first_name`, `second_name` and `year` that should not be used for training the model. Replaces element type with a corresponding integer e.g 'GK' -> 0, 'FWD' -> 3. Replaces any missing values which may occur in the previous season columns with the mean.

`random_forest_regressor.py` - Splits training data into 80% train and 20% test. Fits a RandomForestRegressor model with the training data. Is then evaluated using the Mean Squared Error and R^2 Score. Then saves the model.

`predict_total_points.py` - An implementation of using the AI to predict total points. I used this to test using the model (trained on 2023-24 data) to predict data from 2021-22 and 2022-23 seasons, but this can be updated as required e.g, you train it on all three previously mentioned seasons and use it to predict the 2024-25 season.
