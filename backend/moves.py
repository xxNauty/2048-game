import backend.logic as logic

def move_left(grid):
    new_grid, changed1 = logic.compress(grid)
    new_grid, changed2 = logic.merge(new_grid)
    changed = changed1 or changed2
    new_grid, temp = logic.compress(new_grid)

    return new_grid, changed

def move_right(grid):
    new_grid = logic.reverse(grid)
    new_grid, changed = move_left(new_grid)
    new_grid = logic.reverse(new_grid)

    return new_grid, changed

def move_up(grid):
    new_grid = logic.transpose(grid)
    new_grid, changed = move_left(new_grid)
    new_grid = logic.transpose(new_grid)

    return new_grid, changed

def move_down(grid):
    new_grid = logic.transpose(grid)
    new_grid, changed = move_right(new_grid)
    new_grid = logic.transpose(new_grid)

    return new_grid, changed