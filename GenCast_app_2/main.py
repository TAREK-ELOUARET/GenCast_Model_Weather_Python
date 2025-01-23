import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt

def process_and_visualize(file_accum, file_instant):
    # Load the NetCDF files
    ds_accum = xr.open_dataset(file_accum, engine='netcdf4')
    ds_instant = xr.open_dataset(file_instant, engine='netcdf4')

    # Convert to DataFrame for easier manipulation
    df_accum = ds_accum.to_dataframe().reset_index()
    df_instant = ds_instant.to_dataframe().reset_index()

    # Display column names for both datasets
    print("Accumulated DataFrame columns:", df_accum.columns)
    print("Instantaneous DataFrame columns:", df_instant.columns)

    # Assuming 'valid_time' is the time variable, 't2m' is the temperature variable, and 'tp' is the precipitation variable
    time_var = 'valid_time'
    temperature_var = 't2m'
    precipitation_var = 'tp'

    # Process temperature data
    daily_temp = df_instant.resample('D', on=time_var).agg({
        temperature_var: ['min', 'max']
    }).reset_index()

    # Process precipitation data
    daily_precip = df_accum.resample('D', on=time_var).agg({
        precipitation_var: 'sum'
    }).reset_index()

    # Merge temperature and precipitation data
    daily_data = pd.merge(daily_temp, daily_precip, on=time_var)

    # Flatten the MultiIndex columns
    daily_data.columns = ['date', 'min_temperature', 'max_temperature', 'rainfall']

    # Convert temperatures from Kelvin to Celsius and rainfall from meters to millimeters
    daily_data['min_temperature'] -= 273.15
    daily_data['max_temperature'] -= 273.15
    daily_data['rainfall'] *= 1000

    # Visualize the data
    plot_results(daily_data)

def plot_results(daily_data):
    # Extract dates and values for plotting
    dates = pd.to_datetime(daily_data['date'])
    min_temps = daily_data['min_temperature']
    max_temps = daily_data['max_temperature']
    rainfalls = daily_data['rainfall']

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(dates, min_temps, label='Min Temperature (°C)', color='blue')
    plt.plot(dates, max_temps, label='Max Temperature (°C)', color='red')
    plt.bar(dates, rainfalls, label='Rainfall (mm)', color='green', width=1, alpha=0.5)

    # Add labels and legend
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Weather Data Visualization')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    # File paths for the NetCDF files
    file_accum = 'data_stream-oper_stepType-accum.nc'
    file_instant = 'data_stream-oper_stepType-instant.nc'

    # Process and visualize the data
    process_and_visualize(file_accum, file_instant)

if __name__ == "__main__":
    main()
