import random

EASY_BOARD, EASY_MINES = (9,9), 10
MEDIUM_BOARD, MEDIUM_MINES = (16,16), 40
HARD_BOARD, HARD_MINES = (16,30), 99
DIRECTIONS = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]

def generate_board(board_size, mines):
    board = [[0 for _ in range(board_size[1])] for _ in range(board_size[0])]

    # Place mines
    random_mines = random.sample(range(board_size[0] * board_size[1]), mines)
    for mine in random_mines:
        board[mine // board_size[1]][mine % board_size[1]] = -1

    # Update cell values
    for i in range(board_size[0]):
        for j in range(board_size[1]):
            if board[i][j] != -1:
                for direction in DIRECTIONS:
                    x, y = i + direction[0], j + direction[1]
                    if 0 <= x < board_size[0] and 0 <= y < board_size[1] and board[x][y] == -1:
                        board[i][j] += 1
    return board


def print_board(board):
    for row in board:
        for cell in row:
            if cell == -1:
                print('X', end=' ')
            else:
                print(cell, end=' ')
        print()

