from backend import logic

def move_left(game_board):
    new_game_board, changed1 = logic.compress(game_board)
    new_game_board, changed2 = logic.merge(new_game_board)
    changed = changed1 or changed2
    new_game_board, temp = logic.compress(new_game_board)

    return new_game_board, changed

def move_right(game_board):
    new_game_board = logic.reverse(game_board)
    new_game_board, changed = move_left(new_game_board)
    new_game_board = logic.reverse(new_game_board)

    return new_game_board, changed

def move_up(game_board):
    new_game_board = logic.transpose(game_board)
    new_game_board, changed = move_left(new_game_board)
    new_game_board = logic.transpose(new_game_board)

    return new_game_board, changed

def move_down(game_board):
    new_game_board = logic.transpose(game_board)
    new_game_board, changed = move_right(new_game_board)
    new_game_board = logic.transpose(new_game_board)

    return new_game_board, changed