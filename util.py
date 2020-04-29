import random

from pandas import np


def random_percentage(chance):
    return random.randrange(100) < chance * 100


def makeLin(N):
    A = np.zeros((N, N))
    for i in range(0, N):
        for j in range(0, N):
            if abs(j - i) == 1:
                A[i][j] = 1
    return A


def makeFull(N):
    A = np.zeros((N, N))
    for i in range(0, N):
        for j in range(0, N):
            if i != j:
                A[i][j] = 1
    return A
