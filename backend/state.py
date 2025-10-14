import game_status

from dotenv import load_dotenv

load_dotenv()

def get_current_state(game_board):
    max_val = 0
    for i in range(game_status.current_settings['size']):
        for j in range(game_status.current_settings['size']):
            field_val = game_board[i][j]
            if field_val > max_val:
                max_val = field_val
            if field_val == game_status.current_settings['end_value']:
                return 'WIN', max_val

    for i in range(game_status.current_settings['size']):
        for j in range(game_status.current_settings['size']):
            if game_board[i][j] == 0:
                return 'GAME NOT OVER', None

    for i in range(game_status.current_settings['size'] - 1):
        for j in range(game_status.current_settings['size'] - 1):
            if game_board[i][j] == game_board[i + 1][j] or game_board[i][j] == game_board[i][j + 1]:
                return 'GAME NOT OVER', None

    for j in range(game_status.current_settings['size'] - 1):
        if game_board[game_status.current_settings['size'] - 1][j] == game_board[game_status.current_settings['size'] - 1][j + 1]:
            return 'GAME NOT OVER', None

    for i in range(game_status.current_settings['size'] - 1):
        if game_board[i][game_status.current_settings['size'] - 1] == game_board[i + 1][game_status.current_settings['size'] - 1]:
            return 'GAME NOT OVER', None

    return 'LOST', max_val