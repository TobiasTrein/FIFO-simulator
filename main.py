import argparse

import yaml

from memory import Memory
from tandem import Tandem


def main(config_path):
    with open(config_path, "r", encoding='UTF-8') as config:
        init_params = yaml.safe_load(config)

    ##init_params.pop("reps")
    ##memory = Tandem(**init_params)
    ##result_queue = memory.run()

    ##iterations = init_params.pop("iterations")
    reps_chqueue = []
    reps_pqueue = []
    reps_chqueue_total = []
    reps_pqueue_total = []

    reps = init_params.pop("reps")
    for i in range(reps):
        print(f"Starting simulation #{i+1}")
        memory = Tandem(**init_params)
        result_chqueue, result_pqueue = memory.run()

        '''for i, state in enumerate(result_chqueue):
            print("FILA 1")
            print(f"{i}\t{(state / total_chqueue * 100):.2f}%\t{state:.4f}")
        print(f"total\t100%\t{total_chqueue:.4f}\n")
        for i, state in enumerate(result_pqueue):
            print("FILA 2")
            print(f"{i}\t{(state / total_pqueue * 100):.2f}%\t{state:.4f}")
        print(f"total\t100%\t{total_pqueue:.4f}\n")'''
        
        reps_chqueue.append(result_chqueue)
        reps_pqueue.append(result_pqueue)
        reps_chqueue_total.append(sum(result_chqueue))
        reps_pqueue_total.append(sum(result_pqueue))

    print("average Fila 1")
    total = sum(reps_chqueue_total) / reps
    for i, mean in enumerate([sum(column) / len(column) for column in zip(*reps_chqueue)]):
        print(f"{i}\t{(mean / total * 100):.2f}%\t{mean:.4f}")
    print(f"total\t100%\t{total:.4f}\n")

    print("average Fila 2")
    total = sum(reps_pqueue_total) / reps
    for i, mean in enumerate([sum(column) / len(column) for column in zip(*reps_pqueue)]):
        print(f"{i}\t{(mean / total * 100):.2f}%\t{mean:.4f}")
    print(f"total\t100%\t{total:.4f}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Description of your program.")
    parser.add_argument('-c', '--config', type=str,
                        help='YMAL config file path', default="config2.yml")

    args = parser.parse_args()
    main(args.config)
