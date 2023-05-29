import logging
import random
from enum import Enum

import loggin_config


class Direction(Enum):
    IN = 'IN'
    TRAN = 'TRAN'
    OUT = 'OUT'


##random.seed(int(time.time()))
##random.seed(132)

#r = [0.9921, 0.0004, 0.5534, 0.2761, 0.3398, 0.8963, 0.9023, 0.0132,
#     0.4569, 0.5121, 0.9208, 0.0171, 0.2299, 0.8545, 0.6001, 0.2921]


class Process:

    def __init__(self, min_time=0, max_time=0, global_tempo=.0, direction: Direction = Direction.IN, init=None):
        logging.info(f"Initializing process {direction  }")

        self.direction = direction
        if init is not None:
            self.relative_time = init
            self.tempo = self.relative_time
        else:
            ##ran = r.pop(0)
            ran = random.random()
            self.relative_time = (max_time - min_time) * ran + min_time
            self.tempo = self.relative_time + global_tempo

    def __lt__(self, other):
        return self.tempo < other.tempo

    def __repr__(self) -> str:
        return f"Process({self.relative_time=},{self.direction=})"

    def __str__(self) -> str:
        return f"[{self.direction._name_}, {self.tempo}]"
