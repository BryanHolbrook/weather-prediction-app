# Weather Prediction Application
Weather Prediction Application built-in Python using the open-meteo public API.

Weather Prediction Application built in Python. The application uses the open-meteo.com 
public API to collect historical weather information for North Hollywood, CA 
from the previous five years, 2019-2024, to predict potential weather for the 
date of July 10th, 2024. The date may be updated to predict additional weather averages.

Weather data is then stored in a SQLite database and mapped with SQLAlchemy's ORM.
The weather database is then queried to confirm it was stored correctly. 

Three unit tests are available within to confirm the accuracy of the application, its
functions, and class methods.

## Commands, Inputs, and Outputs needed to run program.
___

### Commands:
- Prints 'WeatherData' class weather data for North Hollywood, CA 
from the previous five years, 2019-2024. 
  #### `print(daily_dataframe)`

- Prints instance of weather data for North Hollywood, CA 
from the previous five years, 2019-2024.
  #### `print(daily_dataframe_inst)`


- Saves weather data to database
  #### `weather_data_inst.save_to_db()`


- Call method on WeatherDataQuery to print weather data from weather_data db. 'limit=1' can be updated to show more
  #### `weather_queries.fetch_and_print_weather_data(limit=1)`


### Inputs:

- The following Open-meteo API Link will be used in your 'fetch_data' method to access
the weather data. 
    `https://archive-api.open-meteo.com/v1/archive`


- Open Meteo link with daily weather variables: 
  
  https://open-meteo.com/en/docs/historical-weather-api#latitude=34.1722&longitude=-118.379&start_date=2019-07-10&hourly=&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,wind_speed_10m_max&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=America%2FLos_Angeles


### Outputs:
- The `print(daily_dataframe)` outputs the 'WeatherData' class 
weather data queried from the above api for North Hollywood, CA 
from the previous five years, 2019-2024 in your run environment as
a Python Pandas dataframe.


- The `print(daily_dataframe_inst)` outputs the instance of weather 
data above api for North Hollywood, CA from the previous five years, 
2019-2024 in your run environment as a Python Pandas dataframe.


- The `weather_data_inst.save_to_db()` outputs the instance weather data in 
to your SQLite 'weather_data' database via SQLAlchemy ORM. 


- The`weather_queries.fetch_and_print_weather_data(limit=1)`outputs the 
'WeatherDataQuery' weather data from your 'weather_data' database in your run environment
and is set to 'limit=1' to show the date July 10th 2024's aggregated five years worth of 
data.
