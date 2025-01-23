from data_pipeline import load_and_process_data, get_time_intervals
from model import WeatherModel
import matplotlib.pyplot as plt
import pandas as pd

def plot_results(actual, predictions, earliest, latest):
    dates = pd.to_datetime(actual['date'])
    plt.figure(figsize=(14, 7))

    # Plot actual temperatures
    plt.plot(dates, actual['min_temperature'], label='Actual Min Temp', color='blue')
    plt.plot(dates, actual['max_temperature'], label='Actual Max Temp', color='red')

    # Plot predicted temperatures
    predicted_dates = pd.date_range(start=dates.iloc[0], periods=len(predictions['min_temperature']), freq='D')
    plt.plot(predicted_dates, predictions['min_temperature'], label='Predicted Min Temp', linestyle='--', color='cyan')
    plt.plot(predicted_dates, predictions['max_temperature'], label='Predicted Max Temp', linestyle='--', color='orange')

    # Plot rainfall
    plt.bar(dates, actual['rainfall'], label='Actual Rainfall', color='green', alpha=0.3)

    # Add labels and legend
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Weather Data and Predictions')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Annotate with time interval information
    plt.text(0.05, 0.95, f'Earliest: {earliest}\nLatest: {latest}', transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.show()

def main():
    # File paths for the NetCDF files
    file_accum = '../data/data_stream-oper_stepType-accum.nc'
    file_instant = '../data/data_stream-oper_stepType-instant.nc'

    # Load and process data
    data = load_and_process_data()

    # Get time intervals
    earliest, latest = get_time_intervals(file_accum, file_instant)

    # Initialize and train the weather model
    model = WeatherModel()
    model.train(data)

    # Forecast using the trained model
    forecast_period = pd.date_range(start=data['date'].iloc[-1], periods=30, freq='D')
    predictions = model.predict(forecast_period)

    # Plot actual vs. predicted values
    plot_results(data, predictions, earliest, latest)

if __name__ == "__main__":
    main()
