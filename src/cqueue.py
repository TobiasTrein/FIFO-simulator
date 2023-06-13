import random
from dataclasses import dataclass

from process import Direction, Process

r = [0.3276, 0.8851, 0.1643, 0.5542, 0.6813, 0.7221, 0.9881]

r2 = [0.9921, 0.0004, 0.5534, 0.2761, 0.3398, 0.8963, 0.9023, 0.0132,
      0.4569, 0.5121, 0.9208, 0.0171, 0.2299, 0.8545, 0.6001, 0.2921]

random.seed(1345)


class _QueueStates(list):
    def __init__(self, capacity):
        super().__init__()
        self.extend([.0] * (capacity + 1))

    def __getitem__(self, index):
        if index >= len(self):
            self.extend([0.0] * (index - len(self) + 1))
        return super().__getitem__(index)

    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([0.0] * (index - len(self) + 1))
        super().__setitem__(index, value)


@dataclass
class Queue:
    idx: str
    workers: int
    run: tuple[float, float]
    arrival: tuple[float, float] = None
    capacity: int = 0
    next_idx: str = None

    queue_states: _QueueStates = None
    ocup: int = 0

    global_time: float = .0

    def __post_init__(self):
        self.queue_states = _QueueStates(self.capacity)

    def chooseNext(self):
        if self.next_idx is None:
            return

        if isinstance(self.next_idx, str):
            return self.next_idx

        keys = list(self.next_idx.keys())
        values = list(self.next_idx.values())

        if (outSum := sum(values)) < 1.0:
            keys.append(None)
            values.append(1.0 - outSum)

        chosen_key = random.choices(keys, values)[0]

        return chosen_key

    def update(self, global_time) -> None:
        self.global_time = global_time
        self.queue_states[self.ocup] += global_time - sum(self.queue_states)

    def scheduleIn(self) -> Process:
        # ran = r.pop(0)
        ran = random.random()
        delta = self.arrival[1] - self.arrival[0]
        time = delta * ran + self.arrival[0] + self.global_time
        return Process(self.idx, time, Direction.IN)

    def arriving(self) -> Process:
        if self.capacity is None or self.ocup < self.capacity:
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
