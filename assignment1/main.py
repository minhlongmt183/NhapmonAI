from random import random, choice
from functools import reduce
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

    def is_attack(self, queens):
        for i in range(1, len(queens)):
            for j in range(0,i):
                xi, yi = i, queens[i]
                xj, yj = j, queens[j]

                if yi == yj or abs(xi-xj) == abs(yi - yj):
                    return True
        return False
#   BFS and DFS algorithm verse 0.2:
#   idea: this is just blind search which might loop through all state.
#   algorithm: this algorithm will put collumn index of queens on chess board row by row
#   init-state : a blank chess board (which is a empty list)
#   rule of action: for each state, algorithm will check if it is the soluton, else generate new states by putting queen on collumn and push it into
#                   frontier (Stack if DFS, Queue if BFS). 
#
    def dfs_solved(self):
        if self.size < 1:
            return []

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
                if col not in solution:
                    queen = col
                    new_state = solution.copy()
                    new_state.append(queen)
                    state_list.push(new_state)

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
                if col not in solution:
                    queen = col
                    new_state = solution.copy()
                    new_state.append(queen)
                    state_list.push(new_state)

#   heuristic algorithm verse 1.3:
#       idea : the algorithm is based on gradient hill climb and using some probalistic element
#       algorithm: the algorithm inclue 2 main steps, initialization and search
#           step 1: initialization - try to create a state for searching with as many queens without being attacked as
#                   possible
#           step 2: search - after the init state has been created, the search algorithm will loop through a certain
#                   numbers of action(C2* size). if can't find the solution back to step 1.
#       init state: a list of unorder distinguish integers form 0 - (n-1) (the index of the list is the row and its value is the 
#               collumn that the queen lie on) and two list of 2*n -1 integers store the number of queen on a diagonal
#       rule of action : swap the value of 2 row in the board so that it can remain unconflict in row and collumn
#
    def heuristic_solve(self):
        def attackUpdate(queens, dp, dm):   #return the list of queens which can be attacked by other queens
            lst = []
            for row, col in enumerate(queens):
                plus, minus = row + col, row - col + len(queens) - 1
                if dp[plus] > 1 or dm[minus] > 1: lst.append(row)
            return lst

        def init(n):    #return the initialize state
            lst = [i for i in range(n)] #contain value of collum in the board
            queens = [-1] * n           #contain the location of the queens has location. (-1) if didn't initailiz its collumn 
            dp = [0] * (2 * n - 1)      #contain the numer of queen on forward slash diagonal
            dm = [0] * (2 * n - 1)      #contain the numer of queen on backward slash diagonal
            for i in range(19 * n):     #loop 19 * size time
                if len(lst) == 0: break
                col = choice(lst)       #pick a collumn that hasn't have any queens on (in lst list)
                for j in range(10):     #for each collumn picked, try 10 times to put in the queens list without conflig
                    row = choice(range(n))
                    if queens[row] == -1:
                        plus, minus = row + col, row - col + n - 1
                        if dp[plus] == 0 and dm[minus] == 0:
                            dp[plus], dm[minus] = 1, 1 # if a suitable postion is founded, add it into queens list and remove it from lst
                            queens[row] = col
                            lst.remove(col)
                            break
            for row, col in enumerate(queens): #init the rest of rows in board with a random value pick from lst
                if col < 0:
                    col = choice(lst)  
                    lst.remove(col)
                    queens[row] = col 
                    plus, minus = row + col, row - col + n - 1
                    dp[plus] += 1
                    dm[minus] += 1
            return (queens, dp, dm)

        def solve(n):
            C1, C2 = 0.45, 32   #2 const help the search faster
            while True:
                queens, dp, dm = init(n) #init state
                attacked = attackUpdate(queens, dp, dm) #attacked queens
                fitness = Fitness(dp, dm)   #current fitness
                limit = C1 * fitness        #to avoid book-keeping, the attacked list only update if current's fitness lower than this variable 
                step = 0
                while step <= C2 * n:       #try to find the solutin in C2*n loops, if cant find it, start again
                    if fitness == 0: return queens
                    for row in attacked:    #loop through row locate in attacked list,try to swap with other row to lower the conflicts between queens
                        other = choice(range(n))
                        if swapBetter(row, other, queens, dp, dm):
                            swap(row, other, queens, dp, dm)
                            fitness = Fitness(dp, dm)
                            if fitness < limit: attacked = attackUpdate(queens, dp, dm)
                    step += len(attacked)

        def Fitness(dp, dm):    #return the collision of queens by adding number of queen -1 of all diagonal have more than 2 queens
            cal = lambda x, y: x + (y - 1 if y != 0 else 0)
            return reduce(cal, dm, 0) + reduce(cal, dp, 0)

        def swapBetter(i, j, queens, dp, dm):   #just conciderate 8 diagonals which can be affected if swap 2 rows
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

        def swap(i, j, queens, dp, dm): #perform swap and update the diagonal list
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

        return solve(self.size)

def print_menu():
    print('-'*30, "Solve N_Queen Problem", '-'*30)
    print("1. Solving by DFS search")
    print("2. Solving by BFS search")
    print("3. Solving by Heuristic search")
    print("4. Exit")
    print('-'*81)

def print_solution(solutions, time):
    print("Solution is: ")
    
    for i in range(len(solutions)):
        print("({}, {})".format(i, solutions[i]))
    
    print("--- %s seconds ---" % time)

def main(): #just for UI
    while True:
        print ('*'*100)
        print("We have solved 100.000 queens in 40-70s with herustic search.")
        print("We have solved 25 queens in ~14s with DFS search.")
        print("We have solved 10 queens in ~14s with BFS search.")
        print("please run our code on google colab to ensured it can solve with large number queen")
        
        print ('*'*60)
        print()
        n_queens = int(input("input the number of queens: "))

        if(n_queens < 0 or n_queens in range(2,4)):
            print("n_queens = {} is invalid!, n_queens >= 0 and neither 2 or 3".format(n_queens))
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
            
            start_time = time.time()
            solutions = n_queens_solve.heuristic_solve()
            print_solution(solutions, time.time()-start_time)
            
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Your choice is invalid! [1-4]")
            continue

        cont = input("is continue? (y)")
        if (cont.lower() == 'y'): continue
        else: break

if __name__ == "__main__":
    main()    

