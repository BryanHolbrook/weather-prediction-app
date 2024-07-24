from weather_data import *

# Instance of WeatherData
weather_data_inst = WeatherData(latitude, longitude, start_date, end_date, daily_params)

# Calling the instance methods
weather_data_inst.fetch_data()
weather_data_inst.process_data()
daily_dataframe_inst = weather_data_inst.get_daily_dataframe()

# Individual functions to confirm correct data being returned from WeatherData instance methods
five_year_avg_temp_inst = daily_dataframe_inst['five_year_avg_temp_for_july_10'].head(1)
five_year_max_wind_speed_inst = daily_dataframe_inst['five_year_max_wind_speed_for_july_10'].head(1)
five_year_sum_precipitation_inst = daily_dataframe_inst['five_year_sum_precip_for_july_10'].head(1)

# Print instance of WeatherData class, calling its methods, and presenting data in a dataframe
print(daily_dataframe_inst.head())

# Print statement to individually review the WeatherClass instance methods and presenting their data in a dataframe
print(five_year_avg_temp_inst)
print(five_year_max_wind_speed_inst)
print(five_year_sum_precipitation_inst)






