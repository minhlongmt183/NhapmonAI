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
        # Caculate the profit to other packages

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
        shipper = [[-1,-1] for i in range(shipperNum)]
        costs = [0] * shipperNum
        safe = [*range(amount)]
        for i in shipper:
            chosen = safe[min(i[-2] )]


    def crossover(parentA, parentB):
        packagePA       = parentA[0]
        idxBreaklstA    = parentA[1]

        packagePB       = parentB[0]
        idxBreaklstB    = parentB[1]

        idxBegin        = 0
        idxEnd          = 0

        while (idxBegin >= idxEnd):
            idxBegin    = randint(0, amount -1)
            idxEnd      = randint(0, amount -1)
        
        packageChild    = [None]*amount
        for i in range(idxBegin, idxEnd+1):
            packageChild[i] = packagePA[i]
            packagePB.remove(packagePA[i])
        
        for i in range(amount):
            if not packageChild[i]:
                packageChild[i] = packagePB[0]
                packagePB       = packagePB[1:]
            
        
        while True:
            idxBegin    = randint(0, shipperNum - 2)
            idxEnd      = randint(0, shipperNum - 2)

            if (idxBegin < idxEnd):
                break
        
        idxBreaklstChild = [None]*(shipperNum-1)
        for i in range(idxBegin, idxEnd+1):
            idxBreaklstChild[i] = idxBreaklstA[i]
        
        for i in range(shipperNum-1):
            if not idxBreaklstChild[i]:
                idxBreaklstChild[i] = idxBreaklstB[0]
                idxBreaklstB        = idxBreaklstB[1:]

    
        return [packageChild, idxBreaklstChild]

    def Mutation(package):
        packagelst      = package[0]
        idxBreaklst     = package[1]
        
        if (np.random.random(1)[0] <= 0.5):
            # method1
            while True:
                idxBegin    = randint(0, len(packagelst)-1)
                idxEnd      = randint(0, len(packagelst)-1)

                if (idxBegin < idxEnd):
                    break

            newPackagelst   = packagelst[:idxBegin] + (packagelst[idxBegin:(idxEnd+1)])[::-1] + packagelst[(idxEnd+1):]
        else:

            #   method 2
            while True:
                idx1    = randint(0, len(packagelst)-1)
                idx2    = randint(0, len(packagelst)-1)

                if (idx1 > 0) and (idx1 < idx2):
                    break

            # part1 = packagelst[:idx1]
            # part2 = packagelst[idx1:(idx2+1)]
            # part3 = packagelst[(idx2+1):]
            
            newPackagelst = packagelst[idx1:(idx2+1)] + packagelst[:idx1] + packagelst[(idx2+1):]

        newIdxBreaklst = []
        for i in range(idxBreaklst):
            while True:
                newidx = randint(0,len(packagelst)-1)
                if newidx not in newIdxBreaklst:
                    newIdxBreaklst.append(newidx)
                    break
                
        return [newPackagelst, newIdxBreaklst]



    def solve():
        pass
        # nonlocal location ,amount,shipperNum ,packages, weightMatrix, offset

        # while True:

    readInput("input.txt")

    initialState()
    Fiteness()
    Selection()
    Crossover()
    Mutation()

    # mapNode()


assign()
