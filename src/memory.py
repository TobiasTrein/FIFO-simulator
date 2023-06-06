from queue import PriorityQueue

from tabulate import tabulate

from cqueue import Queue
from process import Direction, Process


class Memory:
    def __init__(self, iterations) -> None:
        self.iterations: int = iterations

        self.job_queue: PriorityQueue[Process] = PriorityQueue()
        self.queues: dict[str, Queue] = {}

        self.global_time: float = .0

    def _run(self):
        next_proc = self.job_queue.get()

        self.global_time = next_proc.time

        for queue in self.queues.values():
            queue.update(self.global_time)

        current_q = self.queues[next_proc.queue_idx]

        if next_proc.direction == Direction.IN:
            if (proc := current_q.arriving()) is not None:
                self.job_queue.put(proc)

            self.job_queue.put(current_q.scheduleIn())
        else:
            if (proc := current_q.running()) is not None:
                self.job_queue.put(proc)

            if (next_idx := current_q.chooseNext()) is not None:
                next_q = self.queues[next_idx]
                if (proc := next_q.arriving()) is not None:
                    self.job_queue.put(proc)

    def run(self, process: dict, queues: dict) -> None:
        for k, v in queues.items():
            queue = Queue(k, **v)
            self.queues[k] = queue
            if queue.start:
                first = Process(queue.idx, **process)
                self.job_queue.put(first)

        assert not self.job_queue.empty(), "you must define a start queue"

        for _ in range(self.iterations):
            self._run()

        print()

        statistics = []
        res = []

        for queue in self.queues.values():
            print(f"Queue {queue.idx}\n")
            statistics = [(idx, item, item / self.global_time)
                          for idx, item in enumerate(queue.queue_states)]

            res.append(statistics.copy())
            statistics.append(("Total", self.global_time, 1))

            table = tabulate(statistics, headers=[
                             "Queue state", "Time(seconds)", "Probability"], floatfmt=".2f")
            print(table, "\n")

        return res
