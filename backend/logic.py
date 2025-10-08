import random

def start_game(size):
    mat = []
    for _ in range(size):
        mat.append([0] * size)

    add_new_2(mat, size)
    return mat

def find_empty(mat, size):
    for i in range(size):
        for j in range(size):
            if mat[i][j] == 0:
                return i, j
    return None, None

def add_new_2(mat, size):
    empty_positions = [(i, j) for i in range(size) for j in range(size) if mat[i][j] == 0]
    if not empty_positions:
        return
    r, c = random.choice(empty_positions)
    mat[r][c] = 2

def compress(mat, size):
    changed = False

    new_mat = []
    for _ in range(size):
        new_mat.append([0] * size)

    for i in range(size):
        pos = 0

        for j in range(size):
            if mat[i][j] != 0:
                new_mat[i][pos] = mat[i][j]
                if j != pos:
                    changed = True
                pos += 1

    return new_mat, changed

def merge(mat, size):
    changed = False
    for i in range(size):
        for j in range(size - 1):
            if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                mat[i][j] = mat[i][j] * 2
                mat[i][j + 1] = 0
                changed = True

    return mat, changed

def reverse(mat, size):
    new_mat = []
    for i in range(size):
        new_mat.append([])
        for j in range(size):
            new_mat[i].append(mat[i][size - 1 - j])

    return new_mat

def transpose(mat, size):
    new_mat = []
    for i in range(size):
        new_mat.append([])
        for j in range(size):
            new_mat[i].append(mat[j][i])

    return new_mat