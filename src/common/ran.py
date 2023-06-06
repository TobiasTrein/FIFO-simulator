class Random:
    seed = None

    def __init__(self, seed):
        Random.seed = seed

    @staticmethod
    def generate_random():
        modulus = 2**32
        multiplier = 1103515245
        increment = 12345

        seed = (multiplier * Random.seed + increment) % modulus
        Random.seed = seed
        return seed
