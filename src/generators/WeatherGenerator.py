import random
from enum import Enum


class WeatherGenerator:
    def __init__(self) -> None:
        super().__init__()
        self.weather_types = [
            self.WeatherType.SUNNY,
            self.WeatherType.PARTIALLY_SUNNY,
            self.WeatherType.CLOUDY,
            self.WeatherType.RAINY,
            self.WeatherType.THUNDERSTORM_EXPECTED,
            self.WeatherType.SNOW
        ]
        self.weather = self.weather_types[int(random.randint(0, len(self.weather_types) - 1))]

    def next(self):
        will_change = True if int(random.randint(0, 10)) > 8 else False
        if will_change:
            self.weather = [t for t in self.weather_types if t != self.weather_types][int(random.randint(0, len(self.weather_types) - 2))]
        return self.weather

    class WeatherType(Enum):
        SUNNY = 'Sunny'
        PARTIALLY_SUNNY = 'Partially Sunny'
        CLOUDY = 'Cloudy'
        RAINY = 'Rainy'
        THUNDERSTORM_EXPECTED = 'Thunderstorm expected soon',
        SNOW = 'Snow'
        # etc...


