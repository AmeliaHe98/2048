#!/usr/bin/env python
# encoding: utf-8

from game2048 import*
import random
import sys
import math
import struct

POS_WEIGHT_TEMPLATE = [[8,4,2,1],
                        [4,1,1,1],
                        [2,1,1,1],
                        [1,1,1,1]]

def get_left_empty(board):
    return [(x, y)
            for x in range(board.length)
            for y in range(board.length)
            if board.get(x, y) == 0]


def get_vaild_dirs(board):
    return [SwapDir.LEFT, SwapDir.UP, SwapDir.RIGHT, SwapDir.DOWN]


def monotonicity(board):
    value = 0
    for i in range(board.length - 1):
        if not board.get(0, i) > board.get(0, i + 1):
            return 0
        else:
            value += (board.length - i)*board.get(0, i)
    return value + board.get(0, board.length -1)


def corner(board):
    if board.get(0, 0) == board.max_value:
        return board.get(0, 0)
    else:
        return 0


def order_weight(board):
    global POS_WEIGHT_TEMPLATE
    m = 0
    for i in range(board.length):
        for j in range(board.length):
            if board.get(i, j) != 0:
                m += board.get(i,j)*POS_WEIGHT_TEMPLATE[i][j]
    return m


def empty_weight(board):
    return board.num_of_empty


def max_value_weight(board):
    return math.log(board.total_score + 2, 2)


def evaluation_func(board):
    o = order_weight(board)
    c = corner(board)
    m = monotonicity(board)
    e = empty_weight(board)
    x = max_value_weight(board)*10
    return o + m + c + x


def evaluate(board, depth):
    if depth <= 0 or (board.num_of_empty == 0 and not combinable(board)):
        return evaluation_func(board)

    sum_of_ev = 0
    for x, y in get_left_empty(board):
        for p in [2, 4]:
            board.set(x, y, p)
            for swap_dir in get_vaild_dirs(board):
                board_copy = board.copy()
                _, moved = apply_swap(board_copy, swap_dir)
                if moved:
                    ev = evaluate(board_copy, depth - 1)
                    if p == 2:
                        sum_of_ev += ev * 0.95
                    else:
                        sum_of_ev += ev * 0.05
            board.set(x, y, 0)
    return sum_of_ev


def best_dir(board):
    max_value = -float("inf")
    best = SwapDir.DOWN
    for swap_dir in get_vaild_dirs(board):
        board_copy = board.copy()
        _, moved = apply_swap(board_copy, swap_dir)
        if moved:
            cur_value = evaluate(board_copy, depth=1)
            if cur_value >= max_value:
                max_value = cur_value
                best = swap_dir
    return best


def ai_play(n, target):
    return play(n, target, best_dir)


if __name__ == '__main__':
    win_count = 0
    for i in range(10):
        state = ai_play(4, 1024)
        if state == GameState.WIN:
            win_count += 1
            print ("AI Win!")
        else:
            print ("AI Lose!")
    print ("rate:", win_count/10.0)
    print (POS_WEIGHT_TEMPLATE)
