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
            self.memory_states[self.ocup] += tempo - sum(self.memory_states)
            logging.info(f"{self.name} memory state = {self.memory_states}")

        def is_full(self):
            return self.capacity == self.ocup

        def is_free(self):
            return self.ocup <= self.workers

        def is_waiting(self):
            return self.ocup >= self.workers

        def schedule_in(self, tempo, direction):
            if not self.is_full():
                self.ocup += 1

                if self.is_free():
                    # change direction to next queue
                    return self.run_proc(tempo, direction)

        def schedule_out(self, tempo, direction):
            self.ocup -= 1

            if self.is_waiting():
                return self.run_proc(tempo, direction)

    def __init__(self, ch, p, start_time, iterations):
        self.iterations = iterations

        self.job_queue = PriorityQueue()
        self.chqueue = self.TQueue(*ch)
        self.pqueue = self.TQueue(*p)
        self.start_time = start_time
        self.tempo = .0

    def proc_in(self, tempo: float) -> None:
        logging.info("Running proc_in")

        # update all queues
        self.chqueue.update_mem(tempo)
        self.pqueue.update_mem(tempo)
        self.tempo = tempo

        if (res := self.chqueue.schedule_in(self.tempo, Direction.TRAN)) is not None:
            self.job_queue.put(res)

        self.job_queue.put(self.chqueue.init_proc(self.tempo, Direction.IN))

    def proc_tran(self, tempo: float) -> None:
        logging.info("Running proc_tran")

        self.chqueue.update_mem(tempo)
        self.pqueue.update_mem(tempo)
        self.tempo = tempo

        if (res := self.chqueue.schedule_out(self.tempo, Direction.TRAN)) is not None:
            self.job_queue.put(res)

        if (res := self.pqueue.schedule_in(self.tempo, Direction.TRAN)) is not None:
            self.job_queue.put(res)

    def proc_out(self, tempo: float) -> None:
        logging.info("Running proc_tran")

        self.chqueue.update_mem(tempo)
        self.pqueue.update_mem(tempo)
        self.tempo = tempo

        if (res := self.pqueue.schedule_out(self.tempo, Direction.TRAN)) is not None:
            self.job_queue.put(res)

    def _run(self):
        return

    def run(self):
        self.job_queue.put(Process(init=self.start_time))
        logging.info("job queue = %s", [str(i) for i in self.job_queue.queue])

        for i in tqdm(range(self.iterations)):
            logging.info("--- iteration = %i", i + 1)
            next_proc = self.job_queue.get()

            if next_proc.direction == Direction.IN:
                self.proc_in(next_proc.tempo)
            elif next_proc.direction == Direction.TRAN:
                self.proc_tran(next_proc.tempo)
            else:
                self.proc_out(next_proc.tempo)

        for i, state in enumerate(self.chqueue.memory_states):
            print(f"{i}\t{(state / self.tempo * 100):.2f}%\t{state:.4f}")
        print(f"total\t100%\t{self.tempo:.4f}\n")
        for i, state in enumerate(self.pqueue.memory_states):
            print(f"{i}\t{(state / self.tempo * 100):.2f}%\t{state:.4f}")
        print(f"total\t100%\t{self.tempo:.4f}\n")
