# Them cac thu vien neu can
from functools import reduce
from random import randint,choice,random
from copy import deepcopy as dp
from time import time

def assign(file_input, file_output):
    depot ,amount,shipperNum ,packages,weightMatrix,offset =[None]*4 +[{}] +[0]
    # nonlocal depot ,amount,shipperNum ,packages, Map
    WEIGHT = 4
    VOLUMNE = 3

    def readInput():
        nonlocal depot ,amount,shipperNum ,packages
        file    = open(file_input,"r")
        res     = []
        line    = file.readline()
        while line:
            temp = line.split(" ")
            res += [list(map( lambda x : int(x), temp))]
            line = file.readline()
        
        depot               =(-1,*res[0])
        amount,shipperNum   = res[1]
        packages            = [[i] + ele for i,ele in enumerate(res[2:])]
                      
    def calProfit(begin,package):
        return (
            5  +package[VOLUMNE] + package[WEIGHT]*2
            - (((begin[1]-package[1])**2 +(begin[2]-package[2])**2 )**(1/2))*1/2 
        ) - (10 if begin[0] == -1 else 0)

    def mapNode():
        nonlocal depot ,amount,shipperNum ,packages, weightMatrix
        weightMatrix = [[0]*(amount+1) for i in range(amount + 1)]
        for i in range(-1,amount):
            for j in range(-1,amount):
                if i == j or j == -1:
                    weightMatrix[i][j]  = 0
                else:
                    begin               = depot if i == -1 else packages[i]
                    end                 = packages[j]
                    weightMatrix[i][j]  = calProfit(begin,end)

    def getProfit(pac1,pac2):
        nonlocal depot ,amount,shipperNum ,packages, weightMatrix
        return weightMatrix[pac1][pac2]

    def fakeFitness(costs):
        nonlocal shipperNum
        temp    = costs.copy()
        temp.sort()

        res     = 0

        for i ,val in enumerate(temp):
            res += (-val)*(shipperNum -1 -i) + (val*i)
        return res

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
        
        part3   = []
        profit  = getProfit(-1,part1[0])

        for i in range(1,amount):
            if i in part2:
                part3   += [profit]
                profit   = getProfit(-1,part1[i])
            else:
                profit  += getProfit(part1[i-1],part1[i])

        return part3 + [profit]

    def initPop(n):
        nonlocal amount,shipperNum
        template    = [*range(amount)]
        res         = []
        for _ in range(n):
            breaks = []
            while len(breaks) < shipperNum -1:
                temp = randint(1,amount -1)
                if temp not in breaks:
                    breaks += [temp]

            breaks.sort()
            
            lst     = template.copy()
            shipper = []
            # Costs   = []

            while lst:
                package      = choice(lst)
                lst.remove(package)
                shipper     +=[package]

            res += [shipper + breaks + part3ADN(shipper,breaks)]
        return res 

    def Selection(candidatesFitnesses):
        totalFitness    = sum(candidatesFitnesses)
        compensation    = [totalFitness - i for i in candidatesFitnesses]

        totalFitness    = sum(compensation)
        p               = random()
        temp            = 0

        for i,f in enumerate(compensation):
            temp += f/totalFitness
            if p <= temp:
                return i
        return 0
    
    def Crossover(shipperA, shipperB, forward):
        nonlocal shipperNum,amount
        pA      = shipperA[:amount]
        pB      = shipperB[:amount]
        breaks  = shipperA[amount:amount + shipperNum-1] if choice([True,False]) else shipperB[amount:amount + shipperNum-1]
        k       = randint(0, amount - 1)
        result  = [k]
        resCost = []
        cost    = getProfit(-1,k)

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
            if len(result) in breaks:
                resCost += [cost]
                cost = getProfit(-1,k)
            else:
                cost+=temp
            result.append(k)
        resCost += [cost]
        # print(result + breaks + resCost)
        return result + breaks + resCost

    def Mutation(ADN):
        nonlocal amount,shipperNum
        packagelst      = ADN[:amount]
        idxBreaklst     = ADN[amount:amount + shipperNum -1]
        # print(idxBreaklst)
        if (random() <= 0.5):
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

    def writeOutput(ADN):
        nonlocal amount,shipperNum
        part1 = ADN[:amount]
        part2 = ADN[amount:shipperNum + amount - 1]
        
        res = []
        index = 0
        for i in part2:
            res += [part1[index:i]]
            index = i
        res += [part1[index:]]
        print(res)
        print()
        with open(file_output,"w") as file:
            file.write("\n".join([" ".join([str(j) for j in i]) for i in res]))
                  
    def mainAlgo():
        nonlocal amount,shipperNum
        N                       = 15
        population              = initPop(N)
        mutationChance          = 0.15
        Best,BestFitness,theOne = population[0],fakeFitness(population[0][amount+shipperNum -1 :]),False
        C                       = 10000
        while C > 0 :
            C -= 1
            if theOne: break
            populationFitness = []
            for candidate in population:
                temp = fakeFitness(candidate[amount+shipperNum -1 :])
                if temp < BestFitness:
                    C           += 500
                    Best         = candidate
                    BestFitness  = temp

                    if temp - 0 < 1e-7:
                        theOne = True
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
        return Best,BestFitness
    
    start = time()
    readInput()
    mapNode()
    temp = mainAlgo()
    print(temp[1])
    writeOutput(temp[0])
    print(f"runtime {time() -start}")

assign("input.txt","output.txt")
# [5, 8, 3, 4, 1, 7, 0, 6, 2, 1, 7