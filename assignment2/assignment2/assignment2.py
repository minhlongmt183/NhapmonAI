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

    def readInput(file_input):
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
                      
    def calProfit(begin,package):
        return (
            5  +package[VOLUMNE] + package[WEIGHT]*2
            - (((begin[1]-package[1])**2 +(begin[2]-package[2])**2 )**(1/2))*1/2 
        ) - (10 if begin[0] == -1 else 0)

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
                    val = calProfit(begin,end)
                    weightMatrix[i][j] = val
                    if val < offset: offset = val
        if offset < 0:
            for i in range(-1,amount):
                for j in range(amount):
                    if i != j:
                        weightMatrix[i][j]-=offset
        print(offset)
        for i,ele in enumerate(weightMatrix):
            print(i,'->',end = ' ')
            for j,weight in enumerate( ele):
                print(j,': ',weight,end = " , ",sep="")
            print('\n')

    def getProfit(pac1,pac2):
        nonlocal location ,amount,shipperNum ,packages, weightMatrix
        return weightMatrix[pac1][pac2]

    def fakeFitness(costs):
        nonlocal shipperNum
        avgCost = sum(costs)/shipperNum
        return reduce(
            lambda x,y : x+ abs(y - avgCost),
            costs,0
        )

    def Latter(lst,k):
        res = 0
        if k == lst[-1]:
            res = choice(lst)
            while res == k:
                res = choice(lst)
        else:
            res = lst[lst.index(k)+1]
        return res
    
    def Former(lst,k):
        res = 0
        if k == lst[0]:
            res = choice(lst)
            while res == k:
                res = choice(lst)
        else:
            res = lst[lst.index(k)-1]
        return res

    def part3ADN(part1,part2):
        nonlocal amount,shipperNum
        
        part3 = []
        cost = getProfit(-1,part1[0])
        for i in range(1,amount):
            if i in part2:
                part3 += [cost]
                cost = getProfit(-1,part1[i])
            else:
                cost += getProfit(part1[i-1],part1[i])
        part3 += [cost]
        # print(part1,part2,part3)
        return part3

    def initPop(n):
        nonlocal amount,shipperNum
        template = [*range(amount)]
        res = []
        for _ in range(n):
            Breaks = []
            while len(Breaks) < shipperNum -1:
                temp = randint(1,amount -1)
                if temp not in Breaks: Breaks+=[temp]
            Breaks.sort()
            
            lst = template.copy()
            shipper = []
            Costs = []
            while lst:
                package = choice(lst)
                lst.remove(package)
                shipper +=[package]
            res += [shipper + Breaks + part3ADN(shipper,Breaks)]
            
        # print(res)
        return res 

    def Selection(CandidatesFitnesses):
        S = sum(CandidatesFitnesses)
        converted = [S-i for i in CandidatesFitnesses]
        S = sum(converted)
        p = random()
        temp = 0
        for i,f in enumerate(converted):
            temp += (f)/S
            if p <= temp:
                return i
        return 0
    
    def Crossover(shipperA, shipperB, forward):
        nonlocal shipperNum,amount
        pA = shipperA[:amount]
        pB = shipperB[:amount]
        Breaks = shipperA[amount:amount + shipperNum-1] if choice([True,False]) else shipperB[amount:amount + shipperNum-1]
        k = randint(0, amount - 1)
        Result = [k]
        resCost = []
        cost = getProfit(-1,k)
        while len(pA) > 1:
            if forward:
                x = Latter(pA,k)
                y = Latter(pB,k)
            else:
                x = Former(pA,k)
                y = Former(pB,k)

            pA.remove(k)
            pB.remove(k)

            dx = getProfit(k,x)
            dy = getProfit(k,y)

            temp = 0
            if dx < dy:
                k = x
                temp = dx
            else:
                k = y
                temp = dy
            if len(Result) in Breaks:
                resCost += [cost]
                cost = getProfit(-1,k)
            else:
                cost+=temp
            Result.append(k)
        resCost += [cost]
        # print(Result + Breaks + resCost)
        return Result + Breaks + resCost

    def Mutation(ADN):
        nonlocal amount,shipperNum
        packagelst      = ADN[:amount]
        idxBreaklst     = ADN[amount:amount + shipperNum -1]
        # print(idxBreaklst)
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
        for i in range(len(idxBreaklst)):
            while True:
                newidx = randint(1,len(packagelst)-1)
                if newidx not in newIdxBreaklst:
                    newIdxBreaklst.append(newidx)
                    break
            newIdxBreaklst.sort()
        return newPackagelst + newIdxBreaklst + part3ADN(newPackagelst,newIdxBreaklst)

            
            
    def mainAlgo():
        nonlocal amount,shipperNum
        N = 10
        population = initPop(N)
        mutationChance = 0.15
        Best,BestFitness,theOne  = population[0],fakeFitness(population[0][amount+shipperNum -1 :]),False
        C = 1000
        for _ in range(C):
            if theOne: break
            # populationFitness = [fakeFitness(candidate[amount+shipperNum -1 :]) for candidate in population]
            # if 0.0 in populationFitness:
            populationFitness = []
            for candidate in population:
                temp = fakeFitness(candidate[amount+shipperNum -1 :])
                if temp < BestFitness:
                    Best = candidate
                    BestFitness = temp
                    if temp - 0 < 1e-7: theOne = True
                populationFitness += [temp]
            nextGen = []
            for i in range(N):
                parentA = population[Selection(populationFitness)]
                parentB =  population[Selection(populationFitness)]
                child = Crossover(parentA,parentB,choice([True,False]))
                if random() < mutationChance:
                    child = Mutation(child)
                nextGen += [child]
            population = nextGen
        return Best

    def solve(): 
        pass
    readInput("input.txt")
    mapNode()
    print(mainAlgo())
assign()
