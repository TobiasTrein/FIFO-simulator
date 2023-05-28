import argparse

import yaml

from memory import Memory
from tandem import Tandem

def main(config_path):
    with open(config_path, "r", encoding='UTF-8') as config:
        init_params = yaml.safe_load(config)
        
    iterations = init_params.pop("iterations")
    memory = Tandem(**init_params) 
    result_queue = memory.run(iterations)
    return

    iterations = init_params.pop("iterations")
    # reps_queue = []
    # reps_total = []
    for i in range(init_params.pop("reps")):
        print(f"Starting simulation #{i+1}")
        memory = Memory(**init_params)
        result_queue = memory.run(iterations)
        total = sum(result_queue)
        for i, state in enumerate(result_queue):
            print(f"{i}\t{(state / total * 100):.2f}%\t{state:.4f}")
        print(f"total\t100%\t{total:.4f}\n")
        # reps_queue.append(result_queue)
        # reps_total.append(total)

    # print("mean")
    # total = sum(reps_total) / len(reps_total)
    # for i, mean in enumerate([sum(column) / len(column) for column in zip(*reps_queue)]):
    #     print(f"{i}\t{(mean / total * 100):.2f}%\t{mean:.4f}")
    # print(f"total\t100%\t{total:.4f}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description of your program.")
    parser.add_argument('-c', '--config', type=str,
                        help='YMAL config file path', default="config2.yml")

    args = parser.parse_args()
    main(args.config)
    