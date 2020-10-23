#grid search
import sys
from random import random
import time
class Stack():
    def __init__(self):
        self.frontier = []

    def push(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def is_empty(self):
        return len(self.frontier) == 0

    def pop(self):
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class Queue(Stack):
    def pop(self):
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class NQueens:
    def __init__(self, size):
        self.size = size

    def dfs_solved(self):
        if self.size < 1:
            return []

        # solutions = []    
        
        state_list = Stack()
        state_list.push([])

        while not state_list.is_empty():
            solution = state_list.pop()

            if self.is_attack(solution):
                continue

            row = len(solution)
            if row == self.size:
                return solution

            for col in range(self.size):
                queen = (row, col)
                queens = solution.copy()
                queens.append(queen)
                state_list.push(queens)

    def bfs_solved(self):
        if self.size < 1:
            return []

        state_list = Queue()
        state_list.push([])

        while not state_list.is_empty():
            solution = state_list.pop()

            if self.is_attack(solution):
                continue
            
            row = len(solution)
            if row == self.size:
                return solution
            
            for col in range(self.size):
                queen = (row, col)
                queens = solution.copy()
                queens.append(queen)
                state_list.push(queens)
                

    def is_attack(self, queens):
        for i in range(1, len(queens)):
            for j in range(0,i):
                xi, yi = queens[i]
                xj, yj = queens[j]

                if xi == xj or yi == yj or abs(xi-xj) == abs(yi - yj):
                    return True
        return False

def print_menu():
    print('-'*30, "Solve N_Queen Problem", '-'*30)
    print("1. Solving by DFS search")
    print("2. Solving by BFS search")
    print("3. Solving by Heuristic search")
    print("4. Exit")
    print('-'*81)

def print_solution(solutions, time):
    print("--- %s seconds ---" % time)
    print("Solution is: ")
    for sol in solutions:
        print(sol)

def main():
    while True:
        n_queens = int(input("input the number of queens: "))

        if(n_queens < 0):
            print("n_queens = {} is invalid!, n_queens >= 0".format(n_queens))
            continue


        n_queens_solve = NQueens(n_queens)
        print_menu()
        choice = input("Your choice is: ")

        if choice == '1':
            print("Solving by DFS search")

            start_time = time.time()
            solutions = n_queens_solve.dfs_solved()
            print_solution(solutions, time.time()-start_time)

        elif choice == '2':
            print("Solving by BFS search")


            start_time = time.time()
            solutions = n_queens_solve.bfs_solved()
            print_solution(solutions, time.time()-start_time)

        elif choice == '3':
            print("Solving by Heuristic search")
            solutions = n_queens_solve.heuristic_solved()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Your choice is invalid! [1-4]")
            continue

        cont = input("is continue? (y)")
        if (cont.lower() == 'y'):
            continue
        else:
            break

if __name__ == "__main__":
    main()    

