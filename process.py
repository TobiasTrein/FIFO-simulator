import random
from enum import Enum

r = [.3276, .8851, .1643, .5542, .6813, .7221]


class Direction(Enum):
    IN = 'IN'
    OUT = 'OUT'


class Process:
    ARRIVAL = (1, 2)
    RUNNING = (2, 4)

    def __init__(self, seed, global_time=.0, direction: Direction = Direction.IN, relative_time=None):
        random.seed(seed)
        self.direction = direction
        if relative_time is not None:
            self.relative_time = relative_time
        elif direction == Direction.IN:
            self.relative_time = (
                self.ARRIVAL[1] - self.ARRIVAL[0]) * random.random() + self.ARRIVAL[0] + global_time
        else:
            self.relative_time = (
                self.RUNNING[1] - self.RUNNING[0]) * random.random() + self.RUNNING[0] + global_time

    def __lt__(self, other):
        return self.relative_time < other.relative_time

    def __str__(self) -> str:
        return f"{self.direction.name}\t{'{0:0.4f}'.format(self.relative_time)}"
