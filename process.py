import random
from enum import Enum



class Direction(Enum):
    IN = 'IN'
    OUT = 'OUT'


# random.seed(int(time.time()))
random.seed(1345)

class Process:
    # r = [.3276, .8851, .1643, .5542, .6813, .7221, .9881]
    ARRIVAL = (1, 2)
    RUNNING = (3, 6)

    def __init__(self, global_time=.0, direction: Direction = Direction.IN, relative_time=None):
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

    def __repr__(self) -> str:
        return f"Process({self.relative_time=},{self.direction=})"
    
    def __str__(self) -> str:
        return f"[{self.direction._name_}, {self.relative_time}]"
