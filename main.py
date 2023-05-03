# import argparse
# import os

# from memory import Memory


# def main():
#     """_summary_


#     """
#     parser = argparse.ArgumentParser(description='')
#     parser.add_argument('-k', type=int, help='an integer value for K')
#     parser.add_argument('-c', type=int, help='an integer value for C')
#     parser.add_argument('-a', '--arrival', type=str,
#                         help='arrival interval. e.g. "1..2"')
#     parser.add_argument('-r', '--running', type=str,
#                         help='running interval. e.g. "3..6"')
#     parser.add_argument('-s', '--start', type=float,
#                         help='start time. e.g. 2.0')
#     parser.add_argument('-i', type=int, help='iterations')
#     parser.add_argument('-e', type=int, help='executions')
#     parser.add_argument('-d', type=bool, help='True for debug')
#     args = parser.parse_args()

#     if all(arg is not None for arg in vars(args).values()):
#         logging.debug("Using args")

#         arrival = tuple(map(int, args.arrival.split('..')))
#         running = tuple(map(int, args.running.split('..')))
#         K = args.k
#         C = args.c
#         S = args.start
#         I = args.i
#         E = args.e
#         D = args.d
#     else:
#         logging.debug("Using config file")

#         filename = 'config.txt'
#         if os.path.isfile(filename):
#             with open(filename, 'r') as f:
#                 arrival = tuple(map(int, f.readline().split('..')))
#                 running = tuple(map(int, f.readline().split('..')))
#                 K = int(f.readline().strip())
#                 C = int(f.readline().strip())
#                 S = float(f.readline().strip())
#                 I = int(f.readline().strip())
#                 E = int(f.readline().strip())
#                 D = bool(f.readline().strip().lower() != "false")
#         else:
#             logging.debug("Using defaults")

#             arrival = (1, 2)
#             running = (3, 6)
#             K = 3
#             C = 1
#             S = 2.
#             I = 10
#             E = 5
#             D = True

#     # import pdb; pdb.set_trace()
#     result = []
#     for _ in range(E):
#         result.append(Memory(arrival, running, K, C, S, I, D).run())

#     medias_estados = []
#     per_estados = []
#     matriz_transposta = list(zip(*result))
#     for linha in matriz_transposta:
#         media = sum(linha) / len(linha)
#         medias_estados.append(media)
#     for m in medias_estados:
#         per_estados.append((m/sum(medias_estados)) * 100)

#     for i, linha in enumerate(medias_estados):
#         porcentagem = per_estados[i]
#         media = medias_estados[i]
#         print(f"Estado {i}: {media:0.4f} u.t.\t{porcentagem:.2f}%")

# if __name__ == '__main__':
#     main()


import argparse

import yaml

from memory import Memory

def main(config_path):
    with open(config_path, "r", encoding='UTF-8') as config:
        init_params = yaml.safe_load(config)

    iterations = init_params.pop("iterations") 
    memory = Memory(**init_params)
    memory.run(iterations)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description of your program.")
    parser.add_argument('-c', '--config', type=str,
                        help='YMAL config file path')

    args = parser.parse_args()
    main(args.config)
    