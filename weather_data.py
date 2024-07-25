from weather_model import WeatherDataORM, session
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import numpy as np

# WeatherData Class variables
class WeatherData:
    def __init__(self, latitude, longitude, start_date, end_date,daily_params, temperature_unit="fahrenheit",
                 wind_speed_unit="mph", precipitation_unit="inch", timezone="America/Los_Angeles"):
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.daily_params = daily_params
        self.temperature_unit = temperature_unit
        self.wind_speed_unit = wind_speed_unit
        self.precipitation_unit = precipitation_unit
        self.timezone = timezone

        self.cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        self.client = openmeteo_requests.Client(session=self.retry_session)

        self.response = None
        self.daily_dataframe = None

        self.month = None
        self.day = None
        self.year = None
        self.five_year_avg_temp = None
        self.five_year_min_temp = None
        self.five_year_max_temp = None
        self.five_year_avg_wind_speed = None
        self.five_year_min_wind_speed = None
        self.five_year_max_wind_speed = None
        self.five_year_sum_precip = None
        self.five_year_min_precip = None
        self.five_year_max_precip = None

    def fetch_data(self):
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "daily": self.daily_params,
            "temperature_unit": self.temperature_unit,
            "wind_speed_unit": self.wind_speed_unit,
            "precipitation_unit": self.precipitation_unit,
            "timezone": self.timezone
        }
        responses = self.client.weather_api(url, params=params)
        self.response = responses[0]  # Provides the first response

    def process_data(self):
        if not self.response:
            raise ValueError("No response data to process. Call fetch_data() first.")

        daily = self.response.Daily()
        daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
        daily_temperature_2m_mean = daily.Variables(2).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(3).ValuesAsNumpy()
        daily_wind_speed_10m_max = daily.Variables(4).ValuesAsNumpy()

        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
            ),
            "latitude": latitude,
            "longitude": longitude,
            "temperature_2m_max": daily_temperature_2m_max,
            "temperature_2m_min": daily_temperature_2m_min,
            "temperature_2m_mean": daily_temperature_2m_mean,
            "precipitation_sum": daily_precipitation_sum,
            "wind_speed_10m_max": daily_wind_speed_10m_max
        }
        # Calculates the daily data
        self.daily_dataframe = pd.DataFrame(data=daily_data)

        # Calculates the month, day, and year and creates individual columns in the dataframe
        self.daily_dataframe['month'] = self.daily_dataframe['date'].dt.month
        self.daily_dataframe['day'] = self.daily_dataframe['date'].dt.day
        self.daily_dataframe['year'] = self.daily_dataframe['date'].dt.year

        # Calls methods that calculate 5-year average, min, and max temps in °F for July 10th
        self.daily_dataframe['five_year_avg_temp_for_july_10'] = self.calculate_five_year_avg_temp_for_july_10()
        self.daily_dataframe['five_year_min_temp_for_july_10'] = self.calculate_five_year_min_temp_for_july_10()
        self.daily_dataframe['five_year_max_temp_for_july_10'] = self.calculate_five_year_max_temp_for_july_10()

        # Calls methods that calculate 5-year average, min, and max wind speed in Mph for July 10th
        self.daily_dataframe['five_year_avg_wind_speed_for_july_10'] = self.calculate_five_year_avg_wind_speed_for_july_10()
        self.daily_dataframe['five_year_min_wind_speed_for_july_10'] = self.calculate_five_year_min_wind_speed_for_july_10()
        self.daily_dataframe['five_year_max_wind_speed_for_july_10'] = self.calculate_five_year_max_wind_speed_for_july_10()

        # Calls methods that calculate 5-year average, min, and max precipitation in Inches for July 10th
        self.daily_dataframe['five_year_sum_precip_for_july_10'] = self.calculate_five_year_sum_precip_for_july_10()
        self.daily_dataframe['five_year_min_precip_for_july_10'] = self.calculate_five_year_min_precip_for_july_10()
        self.daily_dataframe['five_year_max_precip_for_july_10'] = self.calculate_five_year_max_precip_for_july_10()

        # Methods calculating 5-year average, min, and max temps for July 10th
    def calculate_five_year_avg_temp_for_july_10(self):
        july_10_avg_temp_df = self.daily_dataframe[(self.daily_dataframe['month'] == 7) & (self.daily_dataframe['day'] == 10)]
        five_year_avg_temp = july_10_avg_temp_df['temperature_2m_mean'].mean()
        return five_year_avg_temp

    def calculate_five_year_min_temp_for_july_10(self):
        july_10_min_temp_df = self.daily_dataframe[(self.daily_dataframe['month'] == 7) & (self.daily_dataframe['day'] == 10)]
        five_year_min_temp = july_10_min_temp_df['temperature_2m_min'].min()
        return five_year_min_temp

    def calculate_five_year_max_temp_for_july_10(self):
        july_10_max_temp_df = self.daily_dataframe[(self.daily_dataframe['month'] == 7) & (self.daily_dataframe['day'] == 10)]
        five_year_max_temp = july_10_max_temp_df['temperature_2m_max'].max()
        return five_year_max_temp

    # Methods calculating 5-year average, min, and max wind speeds for July 10th
    def calculate_five_year_avg_wind_speed_for_july_10(self):
        july_10_avg_wind_speed_df = self.daily_dataframe[(self.daily_dataframe['month'] == 7) & (self.daily_dataframe['day'] == 10)]
        five_year_avg_wind_speed = july_10_avg_wind_speed_df['wind_speed_10m_max'].mean()
        return five_year_avg_wind_speed

    def calculate_five_year_min_wind_speed_for_july_10(self):
        july_10_min_wind_speed_df = self.daily_dataframe[(self.daily_dataframe['month'] == 7) & (self.daily_dataframe['day'] == 10)]
        five_year_min_wind_speed = july_10_min_wind_speed_df['wind_speed_10m_max'].min()
        return five_year_min_wind_speed

    def calculate_five_year_max_wind_speed_for_july_10(self):
        july_10_max_wind_speed_df = self.daily_dataframe[(self.daily_dataframe['month'] == 7) & (self.daily_dataframe['day'] == 10)]
        five_year_max_wind_speed = july_10_max_wind_speed_df['wind_speed_10m_max'].max()
        return five_year_max_wind_speed

        # Methods calculating 5-year sum, min, and max precipitation for July 10th
    def calculate_five_year_sum_precip_for_july_10(self):
        july_10_sum_precip_df = self.daily_dataframe[(self.daily_dataframe['month'] == 7) & (self.daily_dataframe['day'] == 10)]
        five_year_sum_precip = july_10_sum_precip_df['precipitation_sum'].mean()
        return five_year_sum_precip

    def calculate_five_year_min_precip_for_july_10(self):
        july_10_min_precip_df = self.daily_dataframe[(self.daily_dataframe['month'] == 7) & (self.daily_dataframe['day'] == 10)]
        five_year_min_precip = july_10_min_precip_df['precipitation_sum'].min()
        return five_year_min_precip

    def calculate_five_year_max_precip_for_july_10(self):
        july_10_max_precip_df = self.daily_dataframe[(self.daily_dataframe['month'] == 7) & (self.daily_dataframe['day'] == 10)]
        five_year_max_precip = july_10_max_precip_df['precipitation_sum'].max()
        return five_year_max_precip

    def get_daily_dataframe(self):
        if self.daily_dataframe is None:
            raise ValueError("Daily dataframe is not available. Call process_data() first.")
        return self.daily_dataframe

    # Method populating table with WeatherData. Call on main.py
    def save_to_db(self):
        if self.daily_dataframe is None:
            raise ValueError("No data to save. Call fetch_data() and process_data() first.")

        for _, row in self.daily_dataframe.iterrows():
            weather_data = WeatherDataORM(
                latitude=row['latitude'],
                longitude=row['longitude'],

                month=row['month'],
                day=row['day'],
                year=row['year'],

                five_year_avg_temp_for_july_10=row['five_year_avg_temp_for_july_10'],
                five_year_min_temp_for_july_10=row['five_year_min_temp_for_july_10'],
                five_year_max_temp_for_july_10=row['five_year_max_temp_for_july_10'],

                five_year_avg_wind_speed_for_july_10=row['five_year_avg_wind_speed_for_july_10'],
                five_year_min_wind_speed_for_july_10=row['five_year_min_wind_speed_for_july_10'],
                five_year_max_wind_speed_for_july_10=row['five_year_max_wind_speed_for_july_10'],

                five_year_sum_precip_for_july_10=row['five_year_sum_precip_for_july_10'],
                five_year_min_precip_for_july_10=row['five_year_min_precip_for_july_10'],
                five_year_max_precip_for_july_10=row['five_year_max_precip_for_july_10']
            )
            session.add(weather_data)

        session.commit()

# Event location data and 5 year weather data range
latitude = 34.1722
longitude = -118.379
start_date = "2019-07-10"
end_date = "2024-07-10"
daily_params = ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean", "precipitation_sum",
                "wind_speed_10m_max"]


weather_data = WeatherData(latitude, longitude, start_date, end_date, daily_params)
weather_data.fetch_data()
weather_data.process_data()
daily_dataframe = weather_data.get_daily_dataframe()

# Individual functions to confirm correct data being returned from WeatherData class methods
five_year_avg_temp = daily_dataframe['five_year_avg_temp_for_july_10'].head(1)
five_year_max_wind_speed = daily_dataframe['five_year_max_wind_speed_for_july_10'].head(1)
five_year_sum_precipitation = daily_dataframe['five_year_sum_precip_for_july_10'].head(1)

# Print functions to review output in run environment
# print(five_year_avg_temp)
# print(five_year_max_wind_speed)
# print(five_year_sum_precipitation)

# print(daily_dataframe[["temperature_2m_max", "temperature_2m_min"]].head())
# print(daily_dataframe.head())

# To CSV Functions to review data output

#five_year_avg_temp.to_csv('five_year_avg_temp_for_july_10.csv', encoding='utf-8')
#five_year_max_wind_speed.to_csv('five_year_max_wind_speed_for_july_10.csv', encoding='utf-8')
#five_year_sum_precipitation.to_csv('five_year_sum_precip_for_july_10.csv', encoding='utf-8')
#daily_dataframe.to_csv('weather_data_test.csv', encoding='utf-8')
