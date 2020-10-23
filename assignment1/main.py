#grid search
import sys
from random import random
from copy import deepcopy
from time import time
class Stack():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class Queue(Stack):
    def pop(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class State:
    def __init__(self,n):
        self.queens = [i for i in range(n)]
        State.size = n
        temp = lambda x:  [State.randomIndex() for i in range(x)]
        changes = temp(n)
        for i,key in enumerate(temp(n)):
            self.switch(key,changes[i],init = True)

        diagonal ={}
        for row,col in enumerate(self.queens):
            back,front = row-col-n,row+col
            if not diagonal.get(back):
                diagonal[back] = 1
            else:
                diagonal[back]+=1
            if not diagonal.get(front):
                diagonal[front] = 1
            else: 
                diagonal[front]+=1
            
        self.diagonal = diagonal


    def switch(self,*args,init = False):
        
        if not init:
            for i in args:
                self.diagonal[i-self.queens[i]-State.size]-= 1
                self.diagonal[ i+self.queens[i]] -= 1

        self.queens[args[0]],self.queens[args[1]]=self.queens[args[1]],self.queens[args[0]]

        if not init:
            for i in args:
                diagonal = (i-self.queens[i]-State.size,i+self.queens[i])
                for j in diagonal:
                    if self.diagonal.get(j):
                        self.diagonal[j]+=1
                    else :self.diagonal[j]=1

    @classmethod
    def randomIndex(cls,size = None):
        if not size:
            size = cls.size
        return int((random()*(size))%size)
        

    def fitness(self):
        res = 0
        for key in self.diagonal.values():
            if key > 1:
                res += ((key-1)*key)//2
        return -res

    def __eq__(self,other):
        return self.queens == other.queens

    def __repr__(self):
        return str(self.queens) #+ '\n'+ str(list(self.diagonal.values()))

def DFS(n):   
    visited = []    
    A = State(n)
    frontier = Stack()
    frontier.add(A)
    while not frontier.empty():
        cur = frontier.remove()
        print(cur,cur.fitness())
        if cur.fitness() == 0: return cur
        visited.append(cur.queens)
        for i in range(State.size):
            if i != State.size-1:
                for j in range(State.size-1,i,-1):
                    temp = deepcopy(cur)
                    temp.switch(i,j)
                    if not temp.queens in visited:
                        frontier.add(temp)
def main():
    a = time
    print(DFS(10))



start_time = time()
main()
print("--- %s seconds ---" % (time() - start_time))