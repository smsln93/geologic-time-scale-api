from enum import Enum


class Rank(str, Enum):
    SUPEREON = "Supereon"
    EON = "Eon"
    ERA = "Era"
    PERIOD = "Period"
    EPOCH = "Epoch"
    AGE = "Age"

    @property
    def order(self) -> int:
        return {
            Rank.SUPEREON: 1,
            Rank.EON: 2,
            Rank.ERA: 3,
            Rank.PERIOD: 4,
            Rank.EPOCH: 5,
            Rank.AGE: 6
        }[self]