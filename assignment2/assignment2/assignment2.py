# Them cac thu vien neu can
from functools import reduce
from random import randint,choice,random
from copy import deepcopy as dp
from math import e
import numpy as np

history = {}
def log(func):
    def inner(*args):
        global history
        # string =lambda x : "|{:<25}|".format(x) if len(str(x)) < 16 else "|{:<25}|".format(str(x))
        # print(*[string(str(i)) for i in (func.__name__,*args)])
        # print(func.__name__)
        if history.get(func.__name__):
            history[func.__name__] += 1
        else : history[func.__name__] = 0
        return func(*args)
    return inner


def assign():
    location ,amount,shipperNum ,packages,weightMatrix,offset =[None]*4 +[{}] +[0]
    # nonlocal location ,amount,shipperNum ,packages, Map
    WEIGHT = 4
    VOLUMNE = 3
    @log
    def readInput( file_input):
        nonlocal location ,amount,shipperNum ,packages
        file = open(file_input,"r")
        res = []
        line = file.readline()
        while line:
            temp = line.split(" ")
            res += [list(map( lambda x : int(x), temp))]
            line = file.readline()
        # res = list(map( lambda x : int(x), res))

        location =(-1,*res[0])
        amount,shipperNum  = res[1]
        packages = [[i] + ele for i,ele in enumerate(res[2:])]

    @log
    def calPathWeight(begin,package):

        return (
            5  +package[VOLUMNE] + package[WEIGHT]*2
            - (((begin[1]-package[1])**2 +(begin[2]-package[2])**2 )**(1/2))*1/2
        ) - (10 if begin[0] == -1 else 0)

    @log
    def mapNode():
        nonlocal location ,amount,shipperNum ,packages, weightMatrix, offset
        # Map = {f"-1-{i}": costCal((-1,*location),packages[i]) -10 for i in range(amount)}
        weightMatrix = [[0]*(amount+1) for i in range(amount + 1)]
        offset = 0
        for i in range(-1,amount):
            for j in range(-1,amount):
                if i ==j or j == -1:
                    weightMatrix[i][j] = 0
                else:
                    begin = location if i == -1 else packages[i]
                    end = packages[j]
                    val = calPathWeight(begin,end)
                    weightMatrix[i][j] = val
                    if val < offset: offset = val
        if offset < 0:
            for i in range(-1,amount):
                for j in range(amount):
                    if i != j:
                        weightMatrix[i][j]-=offset
        print('\n'.join([str(i) for i in weightMatrix]))



        # for i in range(amount):
        #     for j in range(i+1,amount):
        #         Map[f"{i}-{j}"] = getPathWeight(packages[i],packages[j])
        #         if Map[f"{i}-{j}"] < offset: offset = Map[f"{i}-{j}"]
        #         Map[f"{j}-{i}"] = getPathWeight(packages[j],packages[i])
        #         if Map[f"{j}-{i}"] < offset: offset = Map[f"{j}-{i}"]
        #     Map[f"-1-{i}"] = getPathWeight(location,packages[i])
        #     if Map[f"{-1}-{i}"] < offset: offset = Map[f"{-1}-{i}"]
        # for key in sorted(Map.keys()):
        #     if offset != 0:
        #         Map[key] += abs(offset)
            # print(key,": ",Map[key])
        # print(offset)


    @log
    def getPathWeight(pac1,pac2):
        nonlocal location ,amount,shipperNum ,packages, weightMatrix
        return weightMatrix[pac1][pac2]

    def fakeFitness(shipper,costs):
        nonlocal amount
        avgCost = sum(costs)/amount
        return -reduce(
            lambda x,y : x+ abs(y - avgCost),
            costs,0
        )

    def initState():
        nonlocal location ,amount,shipperNum ,packages, weightMatrix, offset
        shipper = [[-1,-1] for i in range shipperNum]
        costs = [0] * shipperNum
        safe = [*range(amount)]
        for i in shipper:
            chosen = safe[min(i[-2] )]

    def crossover(parent_A, parent_B, forward = True):
        totalPackage = len(parent_A)
        package = np.rand(0, length-1)
        avgCost = AvgCost(parent_A, parent_B)
        result = [package]
        idxBreaklst = []
        shipperRemain = shipperNum 
        cost = 0

        while totalPackage > 1:
            if forward:
                px = Latter(parent_A, package)
                py = Latter(parent_B, package)
            else:
                px = Former(parent_A, package)
                py = Former(parent_B, package)
            
            cx = cost(px)
            cy = cost(py)

            if cx < cy:
                package = px
                cost += cx
            else:
                package = py
                cost += cy
            
            if (cost > avgCost) or (totalPackage < shipperRemain):
                result.append(-1)
                shipperNum -= 1
                cost = cost(0, package)

            result.append(package) 
        while (-1 in result):
            idxBreaklst.append(result.index(-1))
            result.remove(-1)
            
        return [result, idxBreaklst]

    def solve():
        pass
        nonlocal location ,amount,shipperNum ,packages, weightMatrix, offset

        while True:


    readInput("input.txt")
    mapNode()
assign()
