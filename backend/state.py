import os

from dotenv import load_dotenv

load_dotenv()

def get_current_state(mat, size, end_val):
    max_val = 0
    for i in range(size):
        for j in range(size):
            field_val = mat[i][j]
            if field_val > max_val:
                max_val = field_val
            if field_val == end_val:
                return 'WIN', max_val

    for i in range(size):
        for j in range(size):
            if mat[i][j] == 0:
                return 'GAME NOT OVER', None

    for i in range(size - 1):
        for j in range(size - 1):
            if mat[i][j] == mat[i + 1][j] or mat[i][j] == mat[i][j + 1]:
                return 'GAME NOT OVER', None

    for j in range(size - 1):
        if mat[size - 1][j] == mat[size - 1][j + 1]:
            return 'GAME NOT OVER', None

    for i in range(size - 1):
        if mat[i][size - 1] == mat[i + 1][size - 1]:
            return 'GAME NOT OVER', None

    return 'LOST', max_val