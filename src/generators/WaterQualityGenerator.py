import random

MIN_WATER_TEMPERATURE = 0
MAX_WATER_TEMPERATURE = 35


class WaterQualityGenerator:
    def __init__(self) -> None:
        super().__init__()
        self.water_quality = WaterQuality()

    def next(self):
        will_change = int(random.randint(0, 10)) > 5
        if will_change:
            temperature = min(max(MIN_WATER_TEMPERATURE, self.water_quality.temperature + int(random.randint(0, 3))), MAX_WATER_TEMPERATURE)
            oxygen_level = min(max(0., self.water_quality.oxygen_level + float(random.uniform(0, 0.1))), 1)
            contamination_level = min(max(0., self.water_quality.contamination_level + float(random.uniform(0, 0.1))), 1)
            self.water_quality.temperature = temperature
            self.water_quality.oxygen_level = oxygen_level
            self.water_quality.contamination_level = contamination_level
        return self.water_quality


class WaterQuality:
    def __init__(self) -> None:
        super().__init__()
        self.temperature = int(random.randint(MIN_WATER_TEMPERATURE, MAX_WATER_TEMPERATURE))
        self.oxygen_level = float(random.uniform(0, 1))
        self.contamination_level = float(random.uniform(0, 1))
