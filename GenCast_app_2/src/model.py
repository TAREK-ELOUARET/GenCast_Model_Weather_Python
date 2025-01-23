from sklearn.linear_model import LinearRegression
import numpy as np

class WeatherModel:
    def __init__(self):
        self.model_min_temp = LinearRegression()
        self.model_max_temp = LinearRegression()
        self.model_rainfall = LinearRegression()

    def train(self, data):
        # Prepare training data
        X = np.arange(len(data)).reshape(-1, 1)
        y_min_temp = data['min_temperature'].values
        y_max_temp = data['max_temperature'].values
        y_rainfall = data['rainfall'].values

        # Train models
        self.model_min_temp.fit(X, y_min_temp)
        self.model_max_temp.fit(X, y_max_temp)
        self.model_rainfall.fit(X, y_rainfall)
        print("Model training completed.")

    def predict(self, days):
        X_future = np.arange(len(days)).reshape(-1, 1)
        min_temp_predictions = self.model_min_temp.predict(X_future)
        max_temp_predictions = self.model_max_temp.predict(X_future)
        rainfall_predictions = self.model_rainfall.predict(X_future)

        predictions = {
            "min_temperature": min_temp_predictions,
            "max_temperature": max_temp_predictions,
            "rainfall": rainfall_predictions
        }
        return predictions
