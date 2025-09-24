import os

from dotenv import load_dotenv

load_dotenv()

def get_current_state(mat):
    max_val = 0
    for i in range(4):
        for j in range(4):
            field_val = mat[i][j]
            if field_val > max_val:
                max_val = field_val
            if field_val == int(os.getenv("END_OF_GAME_VALUE")):
                return 'WON', max_val

    for i in range(4):
        for j in range(4):
            if mat[i][j] == 0:
                return 'GAME NOT OVER', None

    for i in range(3):
        for j in range(3):
            if mat[i][j] == mat[i + 1][j] or mat[i][j] == mat[i][j + 1]:
                return 'GAME NOT OVER', None

    for j in range(3):
        if mat[3][j] == mat[3][j + 1]:
            return 'GAME NOT OVER', None

    for i in range(3):
        if mat[i][3] == mat[i + 1][3]:
            return 'GAME NOT OVER', None

    return 'LOST', max_val