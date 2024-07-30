import unittest
from weather_model import *
from weather_data import *

# Tests confirming instance relationships for 3 different
class TestWeatherData(unittest.TestCase):
    def test_weather_data_query_is_instance(self):
        weather_queries = WeatherDataQuery(self)
        self.assertIsInstance(weather_queries, WeatherDataQuery)

    def test_weather_data_inst_is_instance(self):
        weather_data_inst = WeatherData(latitude, longitude, start_date, end_date, daily_params)
        self.assertIsInstance(weather_data_inst, WeatherData)

    def test_weather_data_is_instance(self):
        weather_data = WeatherData(latitude, longitude, start_date, end_date, daily_params)
        self.assertIsInstance(weather_data, WeatherData)

if __name__ == '__main__':
    unittest.main()
