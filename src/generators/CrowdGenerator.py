import random


class CrowdGenerator:
    def __init__(self) -> None:
        super().__init__()
        self.crowd = int(random.randint(0, 50))

    def next(self):
        self.crowd = max(0, self.crowd + random.randint(-10, 10))
        return self.crowd
