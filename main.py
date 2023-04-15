import argparse
import os

from memory import Memory


def main():
    """_summary_
    

    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-k', type=int, help='an integer value for K')
    parser.add_argument('-c', type=int, help='an integer value for C')
    args = parser.parse_args()

    if args.k is not None and args.c is not None:
        K = args.k
        C = args.c
    else:
        filename = 'config.txt'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                K = int(f.readline().strip())
                C = int(f.readline().strip())
        else:
            K = 3
            C = 1

    # import pdb; pdb.set_trace()
    Memory(K, C).run()


if __name__ == '__main__':
    main()
