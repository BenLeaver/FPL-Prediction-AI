import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

df = pd.read_csv('training_data/training_data_cleaned.csv')

X = df.drop('total_points', axis=1)
y = df['total_points']

# Split data into training and test sets (e.g. 80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=12
)

rf_model = RandomForestRegressor(
    n_estimators=1000,
    random_state=12     
)

rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R² Score: {r2:.2f}")


# Save predictions with test data
test_data_with_predictions = X_test.copy()
test_data_with_predictions['actual_total_points'] = y_test
test_data_with_predictions['predicted_total_points'] = y_pred

#test_data_with_predictions.to_csv('test_data_with_predictions.csv', index=False)

joblib.dump(rf_model, 'models/random_forest_model_v1.pkl')