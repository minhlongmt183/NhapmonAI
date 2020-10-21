import numpy as np

class ChessBoard:
    def __init__(self, n):
        self.width = n
        self.high = n

class ChessMan:
    def __init__(self, x, y):
        self.coord_x = x
        self.coord_y = y



def isSafe(pos, putted):
    for queen in putted:
        if (queen.coord_x == pos.coord_x) or (queen.coord_y == pos.coord_y):
            return False
        
        if (np.abs(queen.coord_y - pos.coord_y) == np.abs(queen.coord_x - pos.coord_x)):
            return False
    
    return True

def putQueen(pos, putted, board_size):
    if pos >= 0 and pos < board_size:
        if isSafe(pos, putted):
            putted.append(pos)
            
    else:
        print("Bad position")
    
    return putted

