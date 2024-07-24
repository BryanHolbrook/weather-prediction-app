from sqlalchemy import Column, Integer, Float, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Class that creates a table SQLite using the SQLAlchemy ORM module
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

# Creates SQLite database
engine = create_engine('sqlite:///weather_data.db')
Base.metadata.create_all(engine)

# Creates session
Session = sessionmaker(bind=engine)
session = Session()
