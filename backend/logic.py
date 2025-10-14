import random
import game_status

def start_game():
    game_board = []
    for _ in range(game_status.current_settings['size']):
        game_board.append([0] * game_status.current_settings['size'])

    return game_board

def find_empty(game_board):
    for i in range(game_status.current_settings['size']):
        for j in range(game_status.current_settings['size']):
            if game_board[i][j] == 0:
                return i, j
    return None, None

def add_new_2(game_board):
    empty_positions = [(i, j) for i in range(game_status.current_settings['size']) for j in range(game_status.current_settings['size']) if game_board[i][j] == 0]
    if not empty_positions:
        return
    r, c = random.choice(empty_positions)
    game_board[r][c] = 2

def compress(game_board):
    changed = False

    new_game_board = []
    for _ in range(game_status.current_settings['size']):
        new_game_board.append([0] * game_status.current_settings['size'])

    for i in range(game_status.current_settings['size']):
        pos = 0

        for j in range(game_status.current_settings['size']):
            if game_board[i][j] != 0:
                new_game_board[i][pos] = game_board[i][j]
                if j != pos:
                    changed = True
                pos += 1

    return new_game_board, changed

def merge(game_board):
    changed = False
    for i in range(game_status.current_settings['size']):
        for j in range(game_status.current_settings['size'] - 1):
            if game_board[i][j] == game_board[i][j + 1] and game_board[i][j] != 0:
                game_board[i][j] = game_board[i][j] * 2
                game_board[i][j + 1] = 0
                changed = True

    return game_board, changed

def reverse(game_board):
    new_game_board = []
    for i in range(game_status.current_settings['size']):
        new_game_board.append([])
        for j in range(game_status.current_settings['size']):
            new_game_board[i].append(game_board[i][game_status.current_settings['size'] - 1 - j])

    return new_game_board

def transpose(game_board):
    new_game_board = []
    for i in range(game_status.current_settings['size']):
        new_game_board.append([])
        for j in range(game_status.current_settings['size']):
            new_game_board[i].append(game_board[j][i])

    return new_game_board