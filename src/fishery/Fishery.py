class Fishery:
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.is_opened = True

    def open(self):
        self.is_opened = True

    def close(self):
        self.is_opened = False
