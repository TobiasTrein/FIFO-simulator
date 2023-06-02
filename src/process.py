from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    IN = 'IN'
    OUT = 'OUT'


@dataclass
class Process:
    queue_idx: str
    time: float
    direction: Direction = Direction.IN

    def __lt__(self, other):
        return self.time < other.time

    def __str__(self) -> str:
        return f"[{self.time}/{self.queue_idx}/{self.direction}]"
