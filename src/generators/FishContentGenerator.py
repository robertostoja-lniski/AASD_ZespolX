import random


class FishContentGenerator:
    def __init__(self) -> None:
        super().__init__()
        self.fish_content = int(random.randint(0, 500))

    def next(self):
        self.fish_content = max(0, self.fish_content + random.randint(-100, 100))
        return self.fish_content
