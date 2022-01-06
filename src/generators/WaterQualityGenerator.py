import random


class WaterQualityGenerator:
    def __init__(self) -> None:
        super().__init__()
        self.water_quality = float(random.random())

    def next(self):
        will_change = True if int(random.randint(0, 10)) > 8 else False
        if will_change:
            self.water_quality = max(0, self.water_quality - float(random.uniform(0, 0.2)))
        return self.water_quality
