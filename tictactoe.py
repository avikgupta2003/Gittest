"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None

def ThreeinRowHorizontal(board):
    copied_board = copy.deepcopy(board)
    for row in copied_board:
        if len(set(row)) == 1:
           return True
        else:
            return False

def ThreeinRowVertical(board):
    col_1 = []
    col_2 = []
    col_3 = []
    copied_board = copy.deepcopy(board)
    for row in copied_board:
        col_1.append(row[0])
        col_2.append(row[1])
        col_3.append(row[2])
    if len(set(col_1)) == 1:
           return True
    elif len(set(col_2)) == 1:
           return True
    elif len(set(col_3)) == 1:
           return True
    else:
        return False

def ThreeinRowDiagonal(board):
    copied_board = copy.deepcopy(board) 
    diag_1 = []
    diag_2 = []
    count1 = 0
    count2 = 2
    for x in range(3):
        diag_1.append(copied_board[count1][count1])
        diag_2.append(copied_board[count1][count2])
        count1 += 1
        count2 -= 1
    if len(set(diag_1)) == 1:
        return True
    elif len(set(diag_2)) == 1:
        return True
    else:
        return False


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    player_X = 0
    player_O = 0

    for row in board:
        if X in row:
            player_X += row.count(X)

        if O in row:
            player_O += row.count(O)
    if player_X > player_O:
        return O
    else:
        return X
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    allPossibleActions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                allPossibleActions.add((i, j))
    
    return allPossibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    i, j = action
    try:
        if new_board[i][j] is not EMPTY:
            raise IndexError
        else:
            new_board[action[0]][action[1]] = player(new_board)
            return new_board
    except IndexError:
        print("Place already taken")
        

        
    
    



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #This is to check whether there is a three in a row horizontally:
    copied_board = copy.deepcopy(board)
    for row in copied_board:
        if row.count("X") == 3 or row.count("O")== 3:
           return row[0]
    
    
    #This is to check whether there is a three in a row vertically:
    col_1 = []
    col_2 = []
    col_3 = []
    for row in copied_board:
        col_1.append(row[0])
        col_2.append(row[1])
        col_3.append(row[2])
    if len(set(col_1)) == 1:
           return col_1[0]
    elif len(set(col_2)) == 1:
           return col_2[0] 
    elif len(set(col_3)) == 1:
           return col_3[0]
       
    #This is to check whether there is a three in a row diagonally:
    diag_1 = []
    diag_2 = []
    count2 = 2
    for x in range(3):
        diag_1.append(copied_board[x][x])
        diag_2.append(copied_board[x][count2])
        x += 1
        count2 -= 1
    if len(set(diag_1)) == 1:
            return diag_1[0]
    elif len(set(diag_2)) == 1:
            return diag_2[0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    
    elif EMPTY not in board[0] and EMPTY not in board[1] and EMPTY not in board[2]:
            return True
    
    return False
        


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return "1"
        elif winner(board) == O:
            return "-1"
        else:
            return "0"
        
def MaxValue(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, float(MinValue(result(board, action))))
        #if float(v) == 1.0:
            #break
    return v

def MinValue(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, float(MaxValue(result(board, action))))
        #if float(v) == -1.0:
            #break
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    

    elif player(board) == X:
        v_one = MaxValue(board)
        list_of_X_actions = []
        for action in actions(board):
            #if MinValue(board) == v_one:
            if float(MinValue(result(board, action))) == v_one:
                list_of_X_actions.append(action)
                return list_of_X_actions
    else:
        v_two = MinValue(board)
        list_of_O_actions = []
        for action in actions(board):
            #if MaxValue(result(board, action))== v_two:
            if float(MaxValue(result(board, action))) == v_two:
                list_of_O_actions.append(action)
                return list_of_O_actions