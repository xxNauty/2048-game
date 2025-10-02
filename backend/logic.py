import os
import random
from dotenv import load_dotenv

load_dotenv()

size = int(os.getenv("GAMEBOARD_SIZE"))

def start_game():
    mat = []
    for _ in range(size):
        mat.append([0] * size)

    print("Commands are as follows : ")
    print("'W' or '↑' : Move Up")
    print("'S' or '↓' : Move Down")
    print("'A' or '←' : Move Left")
    print("'D' or '→' : Move Right")

    add_new_2(mat)
    return mat

def find_empty(mat):
    for i in range(size):
        for j in range(size):
            if mat[i][j] == 0:
                return i, j
    return None, None

def add_new_2(mat):
    if all(all(cell != 0 for cell in row) for row in mat):
        return

    tries = 0
    while tries < 30:
        r = random.randint(0, size - 1)
        c = random.randint(0, size - 1)
        if mat[r][c] == 0:
            mat[r][c] = 2
            return
        tries += 1

    r, c = find_empty(mat)
    if r is not None and c is not None:
        mat[r][c] = 2

def compress(mat):
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

def merge(mat):
    changed = False
    for i in range(size):
        for j in range(size - 1):
            if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                mat[i][j] = mat[i][j] * 2
                mat[i][j + 1] = 0
                changed = True

    return mat, changed

def reverse(mat):
    new_mat = []
    for i in range(size):
        new_mat.append([])
        for j in range(size):
            new_mat[i].append(mat[i][size - 1 - j])

    return new_mat

def transpose(mat):
    new_mat = []
    for i in range(size):
        new_mat.append([])
        for j in range(size):
            new_mat[i].append(mat[j][i])

    return new_mat