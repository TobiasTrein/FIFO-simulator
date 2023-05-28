import logging
from dataclasses import dataclass
from queue import PriorityQueue

from tqdm import tqdm

import loggin_config
from process import Direction, Process


class Tandem:
    @dataclass
    class TQueue:
        name: str
        arrival: tuple[float, float]
        running: tuple[float, float]
        capacity: int
        workers: int

        memory_states: list[float] = None
        ocup: int = 0

        def __post_init__(self):
            self.memory_states = [.0 for _ in range(self.capacity + 1)]

        def init_proc(self, tempo, direction):
            return Process(*self.arrival, tempo, direction)

        def run_proc(self, tempo, direction):
            return Process(*self.running, tempo, direction)

        def update_mem(self, tempo):
            logging.debug(f"{tempo=},{sum(self.memory_states)=}")
            self.memory_states[self.ocup] += tempo - sum(self.memory_states)
            logging.info(f"{self.name} memory state = {self.memory_states}")

        def is_full(self):
            return self.capacity == self.ocup

        def is_free(self):
            return self.ocup <= self.workers

        def is_waiting(self):
            return self.ocup >= self.workers

    def __init__(self, ch, p, start_time):
        self.job_queue = PriorityQueue()
        self.chqueue = self.TQueue(*ch)
        self.pqueue = self.TQueue(*p)
        self.start_time = start_time
        self.tempo = .0

    def proc_in(self, tempo: float) -> None:
        logging.info("Running proc_in")

        self.chqueue.update_mem(tempo)
        self.pqueue.update_mem(tempo)
        self.tempo = tempo

        if not self.chqueue.is_full():
            self.chqueue.ocup += 1

            if self.chqueue.is_free():
                self.job_queue.put(self.chqueue.run_proc(
                    self.tempo, Direction.TRAN))
                logging.info("job queue = %s", [str(i)
                                                for i in self.job_queue.queue])

        self.job_queue.put(self.chqueue.init_proc(self.tempo, Direction.IN))
        logging.info("job queue = %s", [str(i)
                                        for i in self.job_queue.queue])

    def proc_tran(self, tempo: float) -> None:
        logging.info("Running proc_tran")

        self.chqueue.update_mem(tempo)
        self.pqueue.update_mem(tempo)
        self.tempo = tempo

        self.chqueue.ocup -= 1

        if self.chqueue.is_waiting():
            self.job_queue.put(self.chqueue.run_proc(
                self.tempo, Direction.TRAN))
            logging.info("job queue = %s", [str(i)
                         for i in self.job_queue.queue])

        if not self.pqueue.is_full():
            self.pqueue.ocup += 1

            if self.pqueue.is_free():
                self.job_queue.put(self.pqueue.run_proc(
                    self.tempo, Direction.OUT))
                logging.info("job queue = %s", [str(i)
                                                for i in self.job_queue.queue])

    def proc_out(self, tempo: float) -> None:
        logging.info("Running proc_tran")

        self.chqueue.update_mem(tempo)
        self.pqueue.update_mem(tempo)
        self.tempo = tempo

        self.pqueue.ocup -= 1

        if self.pqueue.is_waiting():
            self.job_queue.put(self.pqueue.run_proc(
                self.tempo, Direction.OUT))
            logging.info("job queue = %s", [str(i)
                         for i in self.job_queue.queue])
            
    def _run(self):
        return

    def run(self, iterations):
        self.job_queue.put(Process(init=self.start_time))
        logging.info("job queue = %s", [str(i) for i in self.job_queue.queue])

        for i in tqdm(range(iterations)):
            logging.info("--- iteration = %i", i)
            next_proc = self.job_queue.get()

            if next_proc.direction == Direction.IN:
                self.proc_in(next_proc.tempo)
            elif next_proc.direction == Direction.TRAN:
                self.proc_tran(next_proc.tempo)
            else:
                self.proc_out(next_proc.tempo)

        return self.memory_states
