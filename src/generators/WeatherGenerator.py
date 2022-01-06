import json
import random
from enum import Enum


class WeatherGenerator:
    def __init__(self) -> None:
        super().__init__()

        self.weather = Weather()

    def next(self):
        temperature = min(max(-30, self.weather.temperature + int(random.randint(-3, 3))), 40)
        pressure = min(max(950., self.weather.pressure + float(random.uniform(-10, 10))), 1050)
        precipitation_rate = min(max(0., self.weather.precipitation_rate + float(random.uniform(-10, 10))), 100)
        wind_speed = min(max(0., self.weather.wind_speed + float(random.uniform(-10, 10))), 120)
        cloudiness = min(max(0., self.weather.cloudiness + float(random.uniform(-10, 10))), 100)
        self.weather.temperature = temperature
        self.weather.pressure = pressure
        self.weather.precipitation_rate = precipitation_rate
        self.weather.wind_speed = wind_speed
        self.weather.cloudiness = cloudiness
        return self.weather


class Weather:

    def __init__(self) -> None:
        super().__init__()
        self.temperature = int(random.randint(-30, 40))
        self.pressure = float(random.uniform(950, 1050))
        self.precipitation_rate = float(random.uniform(0, 100))
        self.wind_speed = float(random.uniform(0, 120))
        self.cloudiness = float(random.uniform(0, 100))

    def toJSON(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def deserialize(json_str: str):
        obj = json.loads(json_str)
        weather = Weather()

        weather.temperature = obj['temperature']
        weather.pressure = obj['pressure']
        weather.precipitation_rate = obj['precipitation_rate']
        weather.wind_speed = obj['wind_speed']
        weather.cloudiness = obj['cloudiness']
        return weather
