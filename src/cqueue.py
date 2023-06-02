import random
from dataclasses import dataclass

from process import Direction, Process

r = [0.3276, 0.8851, 0.1643, 0.5542, 0.6813, 0.7221, 0.9881]

r2 = [0.9921, 0.0004, 0.5534, 0.2761, 0.3398, 0.8963, 0.9023, 0.0132,
      0.4569, 0.5121, 0.9208, 0.0171, 0.2299, 0.8545, 0.6001, 0.2921]

random.seed(1345)


@dataclass
class Queue:
    idx: str
    capacity: int
    workers: int
    run: tuple[int, int]
    arrival: tuple[int, int] = None
    next_idx: str = None
    start: bool = False

    queue_states: list[float] = None
    ocup: int = 0

    global_time: float = .0

    def __post_init__(self):
        self.queue_states = [.0 for _ in range(self.capacity + 1)]

    def update(self, global_time):
        internal_time = sum(self.queue_states)
        self.global_time = global_time
        self.queue_states[self.ocup] += global_time - internal_time

    def scheduleIn(self) -> Process:
        # ran = r.pop(0)
        ran = random.random()
        delta = self.arrival[1] - self.arrival[0]
        time = delta * ran + self.arrival[0] + self.global_time
        return Process(self.idx, time, Direction.IN)

    def arriving(self) -> Process:
        if self.ocup < self.capacity:
            self.ocup += 1
            if self.ocup <= self.workers:
                return self.scheduleOut()

    def scheduleOut(self) -> Process:
        # ran = r.pop(0)
        ran = random.random()
        delta = self.run[1] - self.run[0]
        time = delta * ran + self.run[0] + self.global_time
        return Process(self.idx, time, Direction.OUT)

    def running(self) -> Process:
        self.ocup -= 1
        if self.ocup >= self.workers:
            return self.scheduleOut()
