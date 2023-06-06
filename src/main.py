import argparse

import yaml

from memory import Memory
from tabulate import tabulate


def main(config_path):
    with open(config_path, "r", encoding='UTF-8') as config:
        init_params = yaml.safe_load(config)

    iterations = init_params.pop("iterations")
    reps = init_params.pop("reps")
    queues: dict = init_params.pop("queues")
    first_proc = init_params.pop("first_proc")

    statistics = []
    mean = []

    for r in range(reps):
        print(f"Running rep #{r + 1}\n")

        memory = Memory(iterations)
        res = memory.run(first_proc, queues)
        statistics.append(res)

    print("Statistics\n")

    for s1 in zip(*statistics):
        s2 = zip(*s1)
        for s in s2:
            mean.append([sum(values) / len(s) for values in zip(*s)])

        table = tabulate(mean, headers=[
            "Queue state", "Time(seconds)", "Probability"], floatfmt=".2f")
        print(table, "\n")
        mean.clear()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Description of your program.")
    parser.add_argument('-c', '--config', type=str,
                        help='YMAL config file path', default="config.yml")

    args = parser.parse_args()
    main(args.config)
