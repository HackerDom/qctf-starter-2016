#!/usr/bin/python3

import numpy
import random
import inverted_special
import sys

MOD = (1 << 16)

class RandomGenerator:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 25173 + 13849) % (1 << 16)
        return self.seed

def getRandomVector(generator, size):
    return numpy.array([[generator.next()] for _ in range(size)])

def generateShiftedMatrixBottom(randomGenerator, n):
    matrix = numpy.matrix(numpy.zeros((n, n)), dtype=int)
    for x in range(n):
        vect = getRandomVector(randomGenerator, n)
        for y in range(x):
            matrix[y, x] = vect[n - x + y];
    return matrix

def generateShiftedMatrixTop(randomGenerator, n):
    matrix = numpy.matrix(numpy.zeros((n, n)), dtype=int)
    for x in range(n):
        vect = getRandomVector(randomGenerator, n)
        for y in range(x, n):
            matrix[y, x] = vect[y - x]
    return matrix

def generateSpecialMatrix(randomGenerator, n):
    shiftedMatrix = generateShiftedMatrixBottom(randomGenerator, n)

    matrix = numpy.matrix(numpy.eye(n), dtype=int)

    for i in range(n):
        for j in range(i):
            matrix[i] = (matrix[i] + matrix[j] * shiftedMatrix[j, i]) % MOD

    return matrix.transpose()

def generateTrueRandomMatrix(n):
    return numpy.matrix([[random.randint(0, MOD - 1) for _ in range(n)] for __ in range(n)], dtype=int)

def generateMatrixBySecret(secret, n):
    matrix = generateTrueRandomMatrix(n)
    firstApproach = getRawSecretFromMatrix(matrix, len(secret))
    assert len(firstApproach) == len(secret)
    assert len(secret) <= n
    for pos, (sec, approach) in enumerate(zip(map(ord, secret), firstApproach)):
        matrix[0, pos] ^= approach ^ sec
    return matrix

def getRawSecretFromMatrix(matrix, msg_len):
    result = [0] * msg_len
    values = matrix.flatten().tolist()[0]
    for i, val in enumerate(values):
        result[i % msg_len] ^= val % 256
        result[i % msg_len] ^= val // 256
    return result

def getSecretFromMatrix(matrix, msg_len):
    result = getRawSecretFromMatrix(matrix, msg_len)
    return ''.join(map(chr, result))

def getMatrixPow(matrix, p):
    if p == 0:
        assert matrix.shape[0] == matrix.shape[1]
        return numpy.matrix(numpy.eye(matrix.shape[0]), dtype=int)
    result = getMatrixPow(matrix, p // 2)
    result = (result * result) % MOD
    if p % 2 == 1:
        result = (result * matrix) % MOD
    return result

def printHexMatrixToFile(matrix, filename):
    toHex = "{:04x}".format
    lines = []
    for row in matrix.tolist():
        lines.append(''.join(map(toHex, row)))
    with open(filename, 'w') as f:
        f.write('\n'.join(lines))
        f.write('\n')

def getMultMatrix(randomGenerator, n):
    multMatrix = (generateShiftedMatrixTop(randomGenerator, n) * generateSpecialMatrix(randomGenerator, n)) % MOD
    return multMatrix

def saveMultMatrixToFile(filename, n, seed):
    randomGenerator = RandomGenerator(seed)
    multMatrix = getMultMatrix(randomGenerator, n)
    with open(filename, 'w') as f:
        f.write('MATRIX = [')
        f.write(',\n'.join(map(str, multMatrix.tolist())))
        f.write(']\n')

def main():
    seed = 35812
    n = 256
    matrix_pow = 2 ** 30

    if len(sys.argv) < 3:
        print("Usage: {} flag output_file".format(sys.argv[0]))
        sys.exit()
    flag = sys.argv[1]
    output_file = sys.argv[2]

    matrix = generateMatrixBySecret(flag, n)
    assert flag == getSecretFromMatrix(matrix, len(flag))

    multMatrix = getMultMatrix(RandomGenerator(seed), n)

    invertedSpecialMatrix = numpy.matrix(inverted_special.MATRIX, dtype=int)

    encodedMatrix = (matrix * getMatrixPow(invertedSpecialMatrix, matrix_pow)) % MOD

    decodedMatrix = (encodedMatrix * getMatrixPow(multMatrix, matrix_pow)) % MOD
    assert getSecretFromMatrix(decodedMatrix, len(flag)) == flag

    printHexMatrixToFile(encodedMatrix, output_file)



    #generator = RandomGenerator(seed)
    #specialMatrix = generateSpecialMatrix(generator, n)

    #sympyMatrix = sympy.Matrix(specialMatrix)
    #inv = sympyMatrix.inv_mod(MOD)

    #print(inv)

if __name__ == '__main__':
    main()

