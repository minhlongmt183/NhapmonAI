from time import time
import random
from functools import reduce
def  randomIndex(n):
    return int((random()*(n))%n)

def dinit(queens):
    n = len(queens)
    dp = [0] * (2*n -1)
    dn = dp.copy()
    for row, col in enumerate(queens):
        plus, minus = row + col, row - col + n - 1
        dp[plus] += 1
        dn[minus] += 1
    return (dp,dn)

def attackUpdate(queens,dp,dn):
    lst = []
    for row, col in enumerate(queens):
        plus, minus = row + col, row - col + len(queens) - 1
        if dp[plus] > 1 or dn[minus] > 1:
            lst.append(row)
    return lst

def solve(n):
        C1, C2 = 0.45, 32
        queens = random.sample(range(n), n)
        lst = [0]*(2*n-1)
        while True:
            queens = queens.copy()
            for i in range(n):
                row = randomIndex(n)
                queens[i],queens[row] = queens[row], queens[i]
            dp, dn = dinit(queens)
            #print(dp,dn)
            attacked = attackUpdate(queens,dp,dn)
            fitness = Fitness(dp,dn)
            limit = C1*fitness
            step = 0
            while step <= C2 * n:
                if fitness == 0: return queens
                for row in attacked:
                   other = random.choice(range(n))
                   if swapBetter(row,other,queens,dp,dn):
                        swap(row,other,queens,dp,dn)
                        fitness = Fitness(dp,dn)
                        if fitness < limit:
                            attacked = attackUpdate(queens,dp,dn)
                step += len(attacked)

def Fitness (dp,dn):
    cal = lambda x, y: x + (y - 1 if y != 0 else 0)
    return reduce(cal,dn,0) + reduce(cal,dp,0)
def swap(i,j,queens,dp,dn):
    n = len(queens)
    dp[i+queens[i]]     -=  1
    dn[i-queens[i]+n-1] -=  1
    dp[j+queens[j]]     -=  1
    dn[j-queens[j]+n-1] -=  1
    
    dp[i+queens[j]]     +=  1
    dn[i-queens[j]+n-1] +=  1
    dp[j+queens[i]]     +=  1
    dn[j-queens[i]+n-1] +=  1
    queens[i],queens[j]=queens[j],queens[i]

def swapBetter(i,j,queens,dp,dn):
    if i == j : return False
    n = len(queens)
    previous =  (   dp[i+queens[i]],
                    dn[i-queens[i]+n-1],
                    dp[j+queens[j]],
                    dn[j-queens[j]+n-1],
                    dp[i+queens[j]],
                    dn[i-queens[j]+n-1],
                    dp[j+queens[i]],
                    dn[j-queens[i]+n-1]
                )
    
    after =     (   dp[i+queens[i]] -1,
                    dn[i-queens[i]+n-1]-1,
                    dp[j+queens[j]] - 1,
                    dn[j-queens[j]+n-1] -1,
                    dp[i+queens[j]] + 1,
                    dn[i-queens[j]+n-1] + 1,
                    dp[j+queens[i]] + 1,
                    dn[j-queens[i]+n-1] +1
                )
    cal = lambda x, y: x + (y - 1 if y != 0 else 0)
    return reduce(cal,previous,0) > reduce(cal,after,0)


start_time = time()
file = open("log.txt",'w')
print(str(solve(2000)))
print("--- %s seconds ---" % (time() - start_time))
