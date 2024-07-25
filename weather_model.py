from sqlalchemy import Column, Integer, Float, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Class creating SQLite table named weather_data using the SQLAlchemy ORM module
class WeatherDataORM(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float)
    longitude = Column(Float)
    month = Column(Integer)
    day = Column(Integer)
    year = Column(Integer)

    five_year_avg_temp_for_july_10 = Column(Float)
    five_year_min_temp_for_july_10 = Column(Float)
    five_year_max_temp_for_july_10 = Column(Float)

    five_year_avg_wind_speed_for_july_10 = Column(Float)
    five_year_min_wind_speed_for_july_10 = Column(Float)
    five_year_max_wind_speed_for_july_10 = Column(Float)

    five_year_sum_precip_for_july_10 = Column(Float)
    five_year_min_precip_for_july_10 = Column(Float)
    five_year_max_precip_for_july_10 = Column(Float)

# Class and query method to return data from the weather_data.db table
class WeatherDataQuery:
    def __init__(self, session):
        self.session = session

    def fetch_and_print_weather_data(self, limit):
        weather_db_results = self.session.query(WeatherDataORM).limit(limit).all()
        for result in weather_db_results:
            print(result.id, result.latitude, result.longitude, result.month, result.day, result.year,
                  result.five_year_avg_temp_for_july_10, result.five_year_min_temp_for_july_10,
                  result.five_year_max_temp_for_july_10, result.five_year_avg_wind_speed_for_july_10,
                  result.five_year_min_wind_speed_for_july_10, result.five_year_max_wind_speed_for_july_10,
                  result.five_year_sum_precip_for_july_10, result.five_year_min_precip_for_july_10,
                  result.five_year_max_precip_for_july_10
                  )

# Creates SQLite database weather_data.db
engine = create_engine('sqlite:///weather_data.db')
Base.metadata.create_all(engine)

# Creates session
Session = sessionmaker(bind=engine)
session = Session()
