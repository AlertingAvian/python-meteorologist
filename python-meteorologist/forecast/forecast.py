import requests
from typing import Tuple, List
from dataclasses import dataclass
from geopy.geocoders import Nominatim

# TODO: Documentation


@dataclass()
class Properties:
    updated: str
    generated_at: str
    update_time: str
    valid_times: str
    elevation: float


@dataclass()
class Period:
    number: int
    name: str  # unused in hourly
    start_time: str
    end_time: str
    is_day_time: bool
    temperature: int
    temp_unit: str
    wind_speed: str
    wind_direction: str
    icon: str
    short_forecast: str
    long_forecast: str  # unused in hourly


@dataclass()
class Forecast:
    properties: Properties
    periods: list  # list of dataclass Period


class Forecaster(object):
    def __init__(self, user_agent: str = '') -> None:
        if len(user_agent) < 1:
            raise TypeError('User Agent is required.')  # maybe change error or make new one
        self.user_agent = user_agent
        self.request_headers = {"User-Agent": f'{self.user_agent}'}
        self.geolocator = Nominatim(user_agent=self.user_agent)

    def __get_coords(self, postal_code: int) -> Tuple[float, float]:
        if type(postal_code) != int or len(postal_code) != 5:  # for now will require postal code until i think of
            raise TypeError('postal_code must be 5 digit postal code as an integer.')           # something better
        location = self.geolocator.geocode(postal_code)
        return location.latitiude, location.longitude

    def __get_gridpoints(self, coords: Tuple[float, float]) -> str:
        url = f'https://api.weather.gov/points/{coords[0]},{coords[1]}'
        response = requests.get(url, self.request_headers)
        if response.status_code != 200:
            response.raise_for_status()
        return response.json()

    def get_forecast(self, postal_code: int, hourly: bool = False) -> dict:
        coords = self.__get_coords(postal_code)
        if hourly:
            forecast_url = self.__get_gridpoints(coords)['properties']['forecastHourly']
        else:
            forecast_url = self.__get_gridpoints(coords)['properties']['forecast']
        response = requests.get(forecast_url, self.request_headers)
        if response.status_code != 200:
            response.raise_for_status()
        r_json = response.json()
        properties = Properties(r_json['properties']['updated'],
                                r_json['properties']['generatedAt'],
                                r_json['properties']['updateTime'],
                                r_json['properties']['validTimes'],
                                r_json['properties']['elevation']['value'])
        periods = []
        for period in r_json['properties']['periods']:
            periods.append(Period(period['number'],
                                  period['name'],
                                  period['startTime'],
                                  period['endTime'],
                                  period['isDaytime'],
                                  period['temperature'],
                                  period['temperatureUnit'],
                                  period['windSpeed'],
                                  period['windDirection'],
                                  period['icon'],
                                  period['shortForecast'],
                                  period['detailedForecast'],))

        return Forecast(properties, periods)

    def get_hourly_forecast(self, postal_code: int):
        return self.get_forecast(postal_code, hourly=True)
