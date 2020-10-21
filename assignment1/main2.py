from random import random
from copy import deepcopy
from math import e
def Fitness(lst):
    diagonal ={}
    res=0
    for row,col in enumerate(lst):
        back,front = row-col-len(lst),row+col
        if not diagonal.get(back): diagonal[back] = 1
        else: diagonal[back]+=1
        if not diagonal.get(front): diagonal[front] = 1
        else: diagonal[front]+=1
    for key in diagonal.values():
        if key > 1:
            res += (key-1)*key//2
    return -res


def simulateAnealing(lst,T,alpha):
    pass

def Heuristic(lst):
    temp = deepcopy(lst)
    pos1 = randomIndex(len(lst))
    pos2 = randomIndex(len(lst))
    while pos2 == pos1:
        pos2 = randomIndex(len(lst))
    temp[pos1],temp[pos2] = temp[pos2],temp[pos1]
    return temp

def solve(n):
    lst = [i for i in range(n)]
    current = Fitness(lst)
    T = 1000
    alpha = 0.89
    while True:
        temp = Heuristic(lst)
        tempFitness = Fitness(temp)
        if tempFitness == 0: return temp
        if tempFitness>current:
            lst,current = temp,tempFitness
            print('change better')
        else:
            p = random()
            if p < e **((tempFitness-current)/(T)):
                lst,current = temp,tempFitness
                print('change worst')
        T = alpha*T
def randomIndex(size):
    return int((random()*(size))%size)


