import random

MIN_TEMPERATURE = -30.
MAX_TEMPERATURE = 40.
MIN_PRESSURE = 950.
MAX_PRESSURE = 1050.
MIN_PRECIPITATION = 0.
MAX_PRECIPITATION = 100.
MIN_WIND_SPEED = 0.
MAX_WIND_SPEED = 120.
MIN_CLOUDINESS = 0.
MAX_CLOUDINESS = 100.


class WeatherGenerator:
    def __init__(self) -> None:
        super().__init__()

        self.weather = Weather()

    def next(self):
        temperature = min(max(MIN_TEMPERATURE, self.weather.temperature + int(random.uniform(-2, 2))), MAX_TEMPERATURE)
        pressure = min(max(MIN_PRESSURE, self.weather.pressure + float(random.uniform(-2, 2))), MAX_PRESSURE)
        precipitation_rate = min(max(MIN_PRECIPITATION, self.weather.precipitation_rate + float(random.uniform(-2, 2))), MAX_PRECIPITATION)
        wind_speed = min(max(MIN_WIND_SPEED, self.weather.wind_speed + float(random.uniform(-2, 2))), MAX_WIND_SPEED)
        cloudiness = min(max(MIN_CLOUDINESS, self.weather.cloudiness + float(random.uniform(-10, 10))), MAX_CLOUDINESS)
        self.weather.temperature = temperature
        self.weather.pressure = pressure
        self.weather.precipitation_rate = precipitation_rate
        self.weather.wind_speed = wind_speed
        self.weather.cloudiness = cloudiness
        return self.weather


class Weather:

    def __init__(self) -> None:
        super().__init__()
        self.temperature = float(random.uniform(MIN_TEMPERATURE, MAX_TEMPERATURE))
        self.pressure = float(random.uniform(MIN_PRESSURE, MAX_PRESSURE))
        self.precipitation_rate = float(random.uniform(MIN_PRECIPITATION, MAX_PRECIPITATION))
        self.wind_speed = float(random.uniform(MIN_WIND_SPEED, MAX_WIND_SPEED))
        self.cloudiness = float(random.uniform(MIN_CLOUDINESS, MAX_CLOUDINESS))
