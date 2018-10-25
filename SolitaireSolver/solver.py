"""
Created on Wed Oct 24 14:30:27 2018

@author: Goncalo de Melo
"""

from search import *
from copy import deepcopy


# TAI content
def c_peg():
    return "O"


def c_empty():
    return "_"


def c_blocked():
    return "X"


def is_empty(e):
    return e == c_empty()


def is_peg(e):
    return e == c_peg()


def is_blocked(e):
    return e == c_blocked()


# TAI pos
def make_pos(l, c):
    return (l, c)


def pos_l(pos):
    return pos[0]


def pos_c(pos):
    return pos[1]


# TAI move
# List [p_initial, p_final]
def make_move(i, f):
    return [i, f]


def move_initial(move):
    return move[0]


def move_final(move):
    return move[1]


def get_content(board, pos):
    return board[pos_l(pos)][pos_c(pos)]


def valid_move(board, p_initial, p_final):
    '''Checks if a move is valid. This means the middle position being peg and
    final position being empty'''
    l_diff = pos_l(p_final) - pos_l(p_initial)
    c_diff = pos_c(p_final) - pos_c(p_initial)
    p_middle = make_pos(pos_l(p_initial) + l_diff//2, pos_c(p_initial) + c_diff//2)
    # if there is a peg in the middle position and the final is empty
    if is_peg(get_content(board,p_middle)) and is_empty(get_content(board,p_final)):
        return True
    return False


def any_valid_move(board, p_initial):
    '''Checks for a given position if there is any possible move (left, right,
    top, bottom)'''
    # Check left
    if pos_c(p_initial) > 1:
        left = make_pos(pos_l(p_initial), pos_c(p_initial)-2)
        if valid_move(board, p_initial, left):
            return True
    # Check right
    if pos_c(p_initial) < len(board[0])-2:
        right = make_pos(pos_l(p_initial), pos_c(p_initial)+2)
        if valid_move(board, p_initial, right):
            return True
    # Check top
    if pos_l(p_initial) > 1:
        top = make_pos(pos_l(p_initial)-2, pos_c(p_initial))
        if valid_move(board, p_initial, top):
            return True
    # Check bottom
    if pos_l(p_initial) < len(board)-2:
        bot = make_pos(pos_l(p_initial)+2, pos_c(p_initial))
        if valid_move(board, p_initial, bot):
            return True

    return False


def board_moves(board):
    '''For a given board returns all the possible moves for each peace in a
    list of moves'''
    possible_moves = []
    lines = len(board)
    cols = len(board[0])
    # For each line
    for i in range(0, lines):
        # For each column
        for j in range(0, cols):
            # If the position has a peg
            if is_peg(board[i][j]):
                # Check move left
                if j-2 >= 0 and is_peg(board[i][j-1]) and is_empty(board[i][j-2]):
                    possible_moves.append([make_pos(i, j), make_pos(i, j-2)])
                # Check move right
                if j+2 < cols and is_peg(board[i][j+1]) and is_empty(board[i][j+2]):
                    possible_moves.append([make_pos(i, j), make_pos(i, j+2)])
                # Check move top
                if i-2 >= 0 and is_peg(board[i-1][j]) and is_empty(board[i-2][j]):
                    possible_moves.append([make_pos(i, j), make_pos(i-2, j)])
                # Check move bottom
                if i+2 < lines and is_peg(board[i+1][j]) and is_empty(board[i+2][j]):
                    possible_moves.append([make_pos(i, j), make_pos(i+2, j)])
    return possible_moves


def board_perform_move(board, move):
    '''Performs a valid move on a given board. It return a new board with the
    required changes due to the move made, this is: the initial position
    becomes empty; the middle position becomes empty; the last position
    now has a peg'''
    # deepcopy since a board is a list of lists
    board_copy = deepcopy(board)
    l_diff = pos_l(move_final(move)) - pos_l(move_initial(move))
    c_diff = pos_c(move_final(move)) - pos_c(move_initial(move))
    # Update content of initial, middle and final position in the board
    board_copy[pos_l(move_initial(move))][pos_c(move_initial(move))] = c_empty()
    board_copy[pos_l(move_initial(move)) + int(l_diff/2)][pos_c(move_initial(move)) + int(c_diff/2)] = c_empty()
    board_copy[pos_l(move_initial(move)) + l_diff][pos_c(move_initial(move)) + c_diff] = c_peg()

    return board_copy


class sol_state:
    def __init__(self, board, pegs=-1, stuck_pegs=-1):
        self.board = board
        self.pegs, self.stuck_pegs = self.update_state()

    def set_pegs(self, pegs):
        self.pegs = pegs

    def set_stuck_pegs(self, stuck_pegs):
        self.stuck_pegs = stuck_pegs

    def get_pegs(self):
        return self.pegs

    def get_stuck_pegs(self):
        return self.stuck_pegs

    def get_board(self):
        return self.board

    def update_state(self):
        '''Calculates the number of pegs and stuck pegs in a board.'''
        pegs = 0
        stuck_pegs = 0
        # For each line
        for i in range(len(self.board)):
            # For each column
            for j in range(len(self.board[0])):
                # If peg at the position
                if is_peg(self.board[i][j]):
                    pegs += 1
                    # If not any possible move then peg is stuck
                    if not any_valid_move(self.board, make_pos(i, j)):
                        stuck_pegs += 1
        return pegs, stuck_pegs

    def __lt__(self, other):
        return self.pegs > other.pegs


class solitaire(Problem):
    """Models a Solitaire problem as a satisfaction problem.
    A solution cannot have more than 1 peg left on the board."""

    def __init__(self, board):
        self.initial = sol_state(board)

    def actions(self, state):
        return board_moves(state.get_board())

    def result(self, state, action):
        return sol_state(board_perform_move(state.get_board(), action))

    def goal_test(self, state):
        return state.get_pegs() == 1

    def h(self, node):
        """Needed for informed search. This heuristic considers the number of
        pegs + number of stuck pegs."""
        state = node.state
        return state.get_pegs() + state.get_stuck_pegs()
