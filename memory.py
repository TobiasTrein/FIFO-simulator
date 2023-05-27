import logging
from tqdm import tqdm

from queue import PriorityQueue
from dataclasses import dataclass

from process import Direction, Process
import loggin_config

@dataclass
class Memory:
    """
    Class for simulating a queue.

    Args:
        arrival (tuple[float, float]): Interval of time for a new job to arrive.
        running (tuple[float, float]): Interval of time for a job to be executed.
        capacity (int): Maximum capacity of the memory.
        workers (int): Number of workers or servers.
        start_time (float): Initial time for the simulation.

    Attributes:
        memory_states (list[float]): Memory state for each possible number of occupied blocks.
        job_queue (PriorityQueue): Jobs that are waiting to be executed.
        server (int): An integer that represents the number of workers being used.
        ocup (int): An integer that represents the number of blocks occupied.
        tempo (float): A float that represents the current time.
        seed (int): An integer that represents the seed for generating random numbers.

    """
    arrival: tuple[float, float]
    running: tuple[float, float]
    capacity: int
    workers: int
    start_time: float

    memory_states: list[float] = None
    job_queue: PriorityQueue = None
    ocup: int = 0
    tempo: float = 0.

    def __post_init__(self):
        self.memory_states = [.0 for _ in range(self.capacity)]
        self.job_queue = PriorityQueue()

        Process.ARRIVAL = self.arrival
        Process.RUNNING = self.running

    def __repr__(self) -> str:
        return f"Memory({Process.ARRIVAL=}, {Process.RUNNING=}, {self.capacity=}, {self.workers=}, {self.start_time=})"

    def proc_in(self, arriving_time: float) -> None:
        """
        Process an incoming job.

        Args:
            t (float): The time of arrival of the job.
        """
        self.memory_states[self.ocup] += arriving_time - self.tempo
        self.tempo = arriving_time

        if self.ocup < self.capacity:
            self.ocup += 1

            if self.ocup <= self.workers:
                self.job_queue.put(
                    Process(self.tempo, Direction.OUT))

        self.job_queue.put(Process(self.tempo, Direction.IN))

    def proc_out(self, arriving_time: float) -> None:
        """
        Process an outcoming job.

        Args:
            t (float): The time of arrival of the job.
        """
        self.memory_states[self.ocup] += arriving_time - self.tempo
        self.tempo = arriving_time

        self.ocup -= 1
        if self.ocup >= self.workers:
            self.job_queue.put(Process(self.tempo, Direction.OUT))

    def run(self, iterations):
        """
        Run the simulation.

        Returns:
            List[float]: The state of the memory at the end of the simulation.
        """
        self.job_queue.put(Process(relative_time=self.start_time))

        for i in tqdm(range(iterations)):
            logging.info("--- iteration = %i", i)
            next_proc = self.job_queue.get()

            if next_proc.direction == Direction.IN:
                self.proc_in(next_proc.relative_time)
            else:
                self.proc_out(next_proc.relative_time)

            logging.info("memory state = %s", self.memory_states)
            logging.info("job queue = %s", [str(i) for i in self.job_queue.queue])
            logging.info("queue = %s", self.ocup)
            logging.debug("tempo = %s", self.tempo)
            logging.debug("memory state sum = %f", sum(self.memory_states))

        return self.memory_states
