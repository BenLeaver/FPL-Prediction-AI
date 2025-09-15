# FPL-Prediction-AI

Project using machine learning to predict the players which are best picks in the Fantasy Premier League (FPL) game.

## Project Versions

### V1B (Current)

- Uses current season FPL API data to make predictions about the total points of players by the end of the season.
- Random Forest model trained on historical seasons, with predictions for current season.
- Improved performance of the data and preprocessing pipeline.
- Fully refactored, maintainable code.
- Folder: [FPL_AI_V1B](FPL_AI_V1b/README.md)

### V1A (Archived)

- My first prototype.
- Useful to see the development process and early feature engineering.
- Folder: [FPL_AI_V1A](FPL_AI_V1a/README.md)

## Predictions

Total Points Predictions made after GW4 using FPL_AI_V1B.
<img src="Screenshots/Predictions_GW4_2025-26.png" alt="GW4 Top 10 Predictions" width="582" height="916">

## Data used?

Many thanks to [Vaastav](https://github.com/vaastav/Fantasy-Premier-League) for providing historical FPL data of each player.  
Data from the 2020-21, 2021-22, 2022-23, 2023-24 and 2024-25 seasons was used to train the model.

Current season predictions are made using the official FPL API.
