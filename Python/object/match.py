from enum import Enum

class MatchType(Enum):
    MATCHTEST = 0
    PRACTICE = 1
    QUALIFICATION = 2
    PLAYOFF = 3

class Match:
    def __init__(self, type: MatchType, number: int, red_1: int, red_2: int, red_3: int, blue_1: int, blue_2: int, blue_3: int):
        self.type = type
        self.number = number
        self.red_1 = red_1
        self.red_2 = red_2
        self.red_3 = red_3
        self.blue_1 = blue_1
        self.blue_2 = blue_2
        self.blue_3 = blue_3