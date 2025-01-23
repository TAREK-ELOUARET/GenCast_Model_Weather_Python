import xarray as xr
import pandas as pd

def load_and_process_data():
    # Define file paths
    file_accum = '../data/data_stream-oper_stepType-accum.nc'
    file_instant = '../data/data_stream-oper_stepType-instant.nc'

    # Load the NetCDF files
    ds_accum = xr.open_dataset(file_accum, engine='netcdf4')
    ds_instant = xr.open_dataset(file_instant, engine='netcdf4')

    # Convert to DataFrame for easier manipulation
    df_accum = ds_accum.to_dataframe().reset_index()
    df_instant = ds_instant.to_dataframe().reset_index()

    # Resample and process data
    daily_temp = df_instant.resample('D', on='valid_time').agg({
        't2m': ['min', 'max']
    }).reset_index(drop=False)

    daily_precip = df_accum.resample('D', on='valid_time').agg({
        'tp': 'sum'
    }).reset_index(drop=False)

    # Flatten the MultiIndex columns
    daily_temp.columns = ['date', 'min_temperature', 'max_temperature']
    daily_precip.columns = ['date', 'rainfall']

    # Convert units: Temperatures from Kelvin to Celsius and rainfall from meters to millimeters
    daily_temp['min_temperature'] -= 273.15
    daily_temp['max_temperature'] -= 273.15
    daily_precip['rainfall'] *= 1000

    # Merge DataFrames on date
    daily_data = pd.merge(daily_temp, daily_precip, on='date', how='outer')

    return daily_data

def get_time_intervals(file_accum, file_instant):
    # Load the NetCDF files
    ds_accum = xr.open_dataset(file_accum, engine='netcdf4')
    ds_instant = xr.open_dataset(file_instant, engine='netcdf4')

    # Extract time data
    time_accum = ds_accum['valid_time'].values
    time_instant = ds_instant['valid_time'].values

    # Find the earliest and latest times
    earliest_time = min(time_accum.min(), time_instant.min())
    latest_time = max(time_accum.max(), time_instant.max())

    return earliest_time, latest_time
