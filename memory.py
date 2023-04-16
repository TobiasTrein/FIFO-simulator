from process import *


class Memory:

    def __init__(self, arrival, running, K: int, C: int, S: float, I:int) -> None:
        self.K = K
        self.C = C
        self.S = S
        self.I = I
        self.memory_states = [.0 for _ in range(K + 1)]
        self.job_queue: list[Process] = []
        self.server = 0
        self.ocup: int = 0
        self.tempo: float = 0.
        
        Process.ARRIVAL = arrival
        Process.RUNNING = running

        self.job_history = []

    def __str__(self) -> str:
        return f"{self.ocup}\tt={'{0:0.4f}'.format(self.tempo)}\t{' '.join(['{0:0.4f}'.format(i) for i in self.memory_states])}"

    def procIn(self, t: float) -> None:
        self.memory_states[self.ocup] += t - self.tempo
        self.tempo = t

        if self.ocup < self.K:
            self.ocup += 1

            if self.server < self.C:
                self.server += 1
                self.job_queue.append(Process(self.tempo, Direction.OUT))

        self.job_queue.append(Process(self.tempo, Direction.IN))

    def procOut(self, t: float) -> None:
        self.memory_states[self.ocup] += t - self.tempo
        self.tempo = t

        self.ocup -= 1
        if self.ocup >= 1:
            self.server -= 1
            self.job_queue.append(Process(self.tempo, Direction.OUT))

    def run(self):
        self.job_queue.append(Process(relative_time=self.S))

        for _ in range(self.I):
            input(":")
            self.job_history += [
                j.relative_time for j in self.job_queue if j.relative_time not in self.job_history]

            self.job_queue.sort()
            next_proc = self.job_queue.pop(0)
            print(f"{next_proc}\t\t{self}")
            
            prev_ids = set(self.job_history)
            curr_ids = set([item.relative_time for item in self.job_queue])
            print(curr_ids)
            print(prev_ids - curr_ids)

            if next_proc.direction == Direction.IN:
                self.procIn(next_proc.relative_time)
            else:
                self.procOut(next_proc.relative_time)
