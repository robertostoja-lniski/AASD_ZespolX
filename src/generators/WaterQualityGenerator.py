import json
import random


class WaterQualityGenerator:
    def __init__(self) -> None:
        super().__init__()
        self.water_quality = WaterQuality()

    def next(self):
        will_change = True if int(random.randint(0, 10)) > 5 else False
        if will_change:
            temperature = min(max(0, self.water_quality.temperature + int(random.randint(0, 3))), 30)
            oxygen_level = min(max(0., self.water_quality.oxygen_level + float(random.uniform(0, 0.2))), 1)
            contamination_level = min(max(0., self.water_quality.contamination_level + float(random.uniform(0, 0.2))), 1)
            self.water_quality.temperature= temperature
            self.water_quality.oxygen_level = oxygen_level
            self.water_quality.contamination_level = contamination_level
        return self.water_quality


class WaterQuality:
    def __init__(self) -> None:
        super().__init__()
        self.temperature = int(random.randint(0, 30))
        self.oxygen_level = float(random.uniform(0, 100))
        self.contamination_level = float(random.uniform(0, 100))

    def toJSON(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def deserialize(json_str: str):
        obj = json.loads(json_str)
        water_quality = WaterQuality()

        water_quality.temperature = obj['temperature']
        water_quality.oxygen_level = obj['oxygen_level']
        water_quality.contamination_level = obj['contamination_level']

        return water_quality
