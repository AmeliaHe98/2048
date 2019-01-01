#!/usr/bin/env python
# encoding: utf-8

import random
import sys


class GameState:
    NORMAL = 0
    WIN    = 1
    LOSE   = 2


class SwapDir:
    LEFT  = 0
    UP    = 1
    RIGHT = 2
    DOWN  = 3


class GameBoard:
    def __init__(self, n):
        self.length = n
        self.board = [0 for i in range(n*n)]
        self.num_of_empty = n*n
        self.max_value = 2
        self.total_score = 0

    def get(self, x, y):
        if x < 0 or y < 0 or x >= self.length or y >= self.length:
            return -1
        return self.board[x*self.length + y]

    def set(self, x, y, value):
        if x < 0 or y < 0 or x >= self.length or y >= self.length:
            return False
        self.board[x*self.length + y] = value

    def copy(self):
        new_board = GameBoard(0)
        new_board.length = self.length
        new_board.num_of_empty = self.num_of_empty
        new_board.max_value = self.max_value
        new_board.total_score = self.total_score
        new_board.board = self.board[:]
        return new_board

    def __len__(self):
        return self.length


def set_random_number(board):
    n = len(board)
    while not board.num_of_empty == 0:
        x = random.randint(0, n - 1)
        y = random.randint(0, n - 1)
        if board.get(x, y) == 0:
            value = random.uniform(0, 1)
            if value < 0.05:
                value = 4
            else:
                value = 2
            board.set(x, y, value)
            board.num_of_empty -= 1
            return True
    return False


def combinable(board):
    for i in range(len(board)):
        print(len(board))
        for j in range(len(board)):
            value = board.get(i, j)
            if value == 0:
                return True
            if value == board.get(i, j + 1):
                return True
            if value == board.get(i + 1, j):
                return True
    return False


def apply_swap(board, swap_dir):
    def xset_cur(i, j, value):
        board.set(i, j, value)
    def yset_cur(i, j, value):
        board.set(j, i, value)
    def xget_cur(i, j):
        return board.get(i, j)
    def yget_cur(i, j):
        return board.get(j, i)

    col_indexs = range(len(board))

    if swap_dir == SwapDir.LEFT:
        get_cur = xget_cur
        set_cur = xset_cur
        delta = 1
    elif swap_dir == SwapDir.RIGHT:
        get_cur = xget_cur
        set_cur = xset_cur
        delta = -1
        col_indexs = col_indexs[::-1]
    elif swap_dir == SwapDir.UP:
        get_cur = yget_cur
        set_cur = yset_cur
        delta = 1
    elif swap_dir == SwapDir.DOWN:
        get_cur = yget_cur
        set_cur = yset_cur
        delta = -1
        col_indexs = col_indexs[::-1]
    else:
        return 0, False

    score = 0
    moved = False
    for i in range(len(board)):
        for j in col_indexs:
            if get_cur(i, j) == 0:
                continue
            k = j + delta
            while get_cur(i, k) == 0:
                k += delta
            if get_cur(i, j) == get_cur(i, k):
                set_cur(i, j, get_cur(i, j)*2)
                set_cur(i, k, 0)
                if get_cur(i, j) > board.max_value:
                    board.max_value = get_cur(i, j)
                score += get_cur(i, j)
                board.num_of_empty += 1
                moved = True
                # print "get score:", get_cur(i, j)

            k = j
            while get_cur(i, k - delta) == 0:
                k -= delta
            if not k == j:
                set_cur(i, k, get_cur(i, j))
                set_cur(i, j, 0)
                moved = True
                # print "move", i, j, "to", i, k

    board.total_score += score
    return score, moved





def init_game(n):
    board = GameBoard(n)
    set_random_number(board)
    return board, GameState.NORMAL


def print_game(board):
    n = len(board)
    sys.stdout.write("  "+"----"*n+"    \n")
    for i in range(n):
        sys.stdout.write("  ")
        for j in range(n):
            value = board.get(i,j)
            if value == 0:
                value = " "
            sys.stdout.write(str(value).rjust(3) + "|")
        sys.stdout.write("    \n")
        sys.stdout.write("   " + "----" * n + "    \n")
    sys.stdout.flush()


def get_swap_dir(board):
    swap_dir = input("your turn:")
    if swap_dir == 'w':
        return SwapDir.UP
    elif swap_dir == 's':
        return SwapDir.DOWN
    elif swap_dir == 'a':
        return SwapDir.LEFT
    elif swap_dir == 'd':
        return SwapDir.RIGHT
    else:
        return None


def play(n, target, swap_func, debug=False):
    board, state = init_game(n)
    set_random_number(board)
    if debug:
        print_game(board)
    while state == GameState.NORMAL:
        if board.max_value >= target:
            state = GameState.WIN
            break
        elif board.num_of_empty == 0 and not combinable(board):
            state = GameState.LOSE
            break

        swap_dir = swap_func(board)
        cur_score, moved = apply_swap(board, swap_dir)
        if moved:
            if debug:
                print ("score:", board.total_score)
                print_game(board)
            set_random_number(board)

    return state


if __name__ == '__main__':
    state = play(5, 2048, get_swap_dir, debug=True)
    if state == GameState.WIN:
        print ("You Win!")
    else:
        print ("You Lose!")