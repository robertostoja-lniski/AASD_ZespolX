import random
from enum import Enum
from typing import Dict


class FishContentGenerator:
    def __init__(self) -> None:
        super().__init__()
        self.fish_content = {
            ft: random.randint(0, 166)
            for ft in [e.value for e in FishType]
        }

    def next(self) -> Dict[str, int]:
        """
        Generates mapping between fish name and the number of fishes of this type.
        :return: The mapping between fish name and the number of fishes of this type.
        """
        for fish_name in self.fish_content:
            self.fish_content[fish_name] = max(0, self.fish_content[fish_name] + random.randint(-33, 33))
        return self.fish_content


class FishType(Enum):
    SALMON = "Salmon"
    CARP = "Carp"
    TUNA = "Tuna"
