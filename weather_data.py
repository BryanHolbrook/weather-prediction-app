import os
import pandas as pd
import datetime as dt

class WeatherData:
    def __init__(self, latitude, longitude, month, day, year, five_year_avg_temp, five_year_min_temp, five_year_max_temp, five_year_avg_wind_speed, five_year_min_wind_speed, five_year_max_wind_speed, five_year_sum_wind_speed, five_year_min_precip, five_year_max_precip):

        self.latitude = latitude
        self.longitude = longitude
        self.month = month
        self.day = day
        self.year = year
        self.five_year_avg_temp = five_year_avg_temp
        self.five_year_min_temp = five_year_min_temp
        self.five_year_max_temp = five_year_max_temp
        self.five_year_avg_wind_speed = five_year_avg_wind_speed
        self.five_year_min_wind_speed = five_year_min_wind_speed
        self.five_year_max_wind_speed = five_year_max_wind_speed
        self.five_year_sum_wind_speed = five_year_sum_wind_speed
        self.five_year_min_precip = five_year_min_precip
        self.five_year_max_precip = five_year_max_precip

weather_day_test = WeatherData(333,444, 12,10,2004, 3, 4, 5, 6, 7, 8, 9, 10, 11)

print(weather_day_test.latitude)