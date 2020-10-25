from time import time
from random import random, choice
from functools import reduce

def attackUpdate(queens, dp, dm):
    lst = []
    for row, col in enumerate(queens):
        plus, minus = row + col, row - col + len(queens) - 1
        if dp[plus] > 1 or dm[minus] > 1:
            lst.append(row)
    return lst

def init(n):
    lst = [i for i in range(n)]
    queens = [-1] * n
    dp = [0] * (2 * n - 1)
    dm = [0] * (2 * n - 1)
    for i in range(19 * n):
        if len(lst) == 0: break
        col = choice(lst)
        for j in range(10):
            row = choice(range(n))
            if queens[row] == -1:
                plus, minus = row + col, row - col + n - 1
                if dp[plus] == 0 and dm[minus] == 0:
                    dp[plus], dm[minus] = 1, 1
                    queens[row] = col
                    lst.remove(col)
                    break
    for row, col in enumerate(queens):
        if col < 0:
            col = choice(lst)
            lst.remove(col)
            queens[row] = col
            plus, minus = row + col, row - col + n - 1
            dp[plus] += 1
            dm[minus] += 1
    return (queens, dp, dm)


def solve(n):
    C1, C2 = 0.45, 32
    queens = [i for i in range(n)]
    while True:
        queens, dp, dm = init(n)
        attacked = attackUpdate(queens, dp, dm)
        fitness = Fitness(dp, dm)
        limit = C1 * fitness
        step = 0
        while step <= C2 * n:
            if fitness == 0: return queens
            for row in attacked:
                other = choice(range(n))
                if swapBetter(row, other, queens, dp, dm):
                    swap(row, other, queens, dp, dm)
                    fitness = Fitness(dp, dm)
                    if fitness < limit:
                        attacked = attackUpdate(queens, dp, dm)
            step += len(attacked)


def Fitness(dp, dm):
    cal = lambda x, y: x + (y - 1 if y != 0 else 0)
    return reduce(cal, dm, 0) + reduce(cal, dp, 0)


def swap(i, j, queens, dp, dm):
    n = len(queens)
    dp[i + queens[i]] -= 1
    dm[i - queens[i] + n - 1] -= 1
    dp[j + queens[j]] -= 1
    dm[j - queens[j] + n - 1] -= 1
    dp[i + queens[j]] += 1
    dm[i - queens[j] + n - 1] += 1
    dp[j + queens[i]] += 1
    dm[j - queens[i] + n - 1] += 1
    queens[i], queens[j] = queens[j], queens[i]


def swapBetter(i, j, queens, dp, dm):
    if i == j: return False
    n = len(queens)
    previous = (dp[i + queens[i]], dm[i - queens[i] + n - 1],
                dp[j + queens[j]], dm[j - queens[j] + n - 1],
                dp[i + queens[j]], dm[i - queens[j] + n - 1],
                dp[j + queens[i]], dm[j - queens[i] + n - 1])

    after = (dp[i + queens[i]] - 1, dm[i - queens[i] + n - 1] - 1,
             dp[j + queens[j]] - 1, dm[j - queens[j] + n - 1] - 1,
             dp[i + queens[j]] + 1, dm[i - queens[j] + n - 1] + 1,
             dp[j + queens[i]] + 1, dm[j - queens[i] + n - 1] + 1)
    cal = lambda x, y: x + (y - 1 if y != 0 else 0)
    return reduce(cal, previous, 0) > reduce(cal, after, 0)


start_time = time()
file = open("log.txt", 'w')
file.write(str(solve(100000)))
print("--- %s seconds ---" % (time() - start_time))
