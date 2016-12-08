#!/usr/bin/python3

import numpy

MOD = 2 ** 16


class RandomGenerator:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 25173 + 13849) % (2 ** 16)
        return self.seed


def get_random_vector(generator, size):
    return numpy.array([[generator.next()] for _ in range(size)])


def convert_matrix(matrix, amount_of_cycles, seed):
    generator = RandomGenerator(seed)
    for i in range(amount_of_cycles):
        rand_vector = get_random_vector(generator, len(matrix))
        new_vector = numpy.dot(matrix, rand_vector)
        matrix = numpy.hstack((matrix[:, 1:], new_vector)) % MOD
    return matrix


def get_initial_matrix(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    n = len(lines[0]) // 4

    matrix = numpy.zeros((n, n), dtype=int)

    for y, line in enumerate(lines):
        tokens = [line[i:i+4] for i in range(0, len(line), 4)]
        for x, token in enumerate(tokens):
            matrix[y][x] = int(token, 16)

    return matrix


def get_secret_from_matrix(matrix, msg_len):
    result = [0] * msg_len
    values = matrix.flatten()
    for i, val in enumerate(values):
        result[i % msg_len] ^= val % 256
        result[i % msg_len] ^= val // 256

    return ''.join(map(chr, result))


def main():
    amount_of_cycles = 2 ** 38
    seed = 35812
    n = 256
    msg_len = 35
    matrix = get_initial_matrix('encryption')
    converted_matrix = convert_matrix(matrix, amount_of_cycles, seed)
    secret = get_secret_from_matrix(converted_matrix, msg_len)
    print(secret)


if __name__ == '__main__':
    main()
