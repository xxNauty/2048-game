import tkinter as tk

import backend.logic as logic
import backend.moves as moves
import backend.state as state
import backend.game_history as game_history

COLORS = {
    0: ("#cdc1b4", "#776e65"),
    2: ("#eee4da", "#776e65"),
    4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"),
    256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
}

count_down = 0
count_up = 0
count_left = 0
count_right = 0

class Game(tk.Frame):
    def __init__(self, master=None, root_window=None):
        super().__init__(master)
        # self.master.title("2048 Game")
        self.root_window = root_window
        self.grid()
        self.size = 4
        self.grid_cells = []
        self.init_grid()
        self.status_label = tk.Label(self, text="", font=("Verdana", 14))
        self.status_label.grid(row=self.size, column=0, columnspan=self.size)
        self.init_game()
        # self.master.bind("<Key>", self.key_down)
        # self.master.geometry("440x600")

    def init_grid(self):
        background = tk.Frame(self, bg="#bbada0")
        background.grid()
        for i in range(self.size):
            row = []
            for j in range(self.size):
                cell = tk.Frame(
                    background,
                    bg=COLORS[0][0],
                    width=100,
                    height=100
                )
                cell.grid(row=i, column=j, padx=5, pady=5)
                t = tk.Label(
                    master=cell,
                    text="",
                    bg=COLORS[0][0],
                    fg=COLORS[0][1],
                    justify="center",
                    font=("Verdana", 24, "bold"),
                    width=4,
                    height=2,
                    relief=tk.RAISED,
                    borderwidth=5
                )
                t.grid()
                row.append(t)
            self.grid_cells.append(row)

    def init_game(self):
        self.mat = logic.start_game()
        self.update_grid()
        self.status_label.config(text="")

    def update_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                value = self.mat[i][j]
                color_bg, color_fg = COLORS.get(value, ("#3c3a32", "#f9f6f2"))
                label = self.grid_cells[i][j]
                label.config(text=str(value) if value else "",bg=color_bg, fg=color_fg)
        self.update_idletasks()

    def key_down(self, event):
        global count_up, count_down, count_right, count_left

        key = event.keysym

        if key in ["Up", "w", "W"]:
            count_up += 1
            self.mat, moved = moves.move_up(self.mat)
        elif key in ["Down", "s", "S"]:
            count_down += 1
            self.mat, moved = moves.move_down(self.mat)
        elif key in ["Left", "a", "A"]:
            count_left += 1
            self.mat, moved = moves.move_left(self.mat)
        elif key in ["Right", "d", "D"]:
            count_right += 1
            self.mat, moved = moves.move_right(self.mat)
        else:
            return

        status, max_value_on_gameboard = state.get_current_state(self.mat)
        if status == "GAME NOT OVER" and moved:
            logic.add_new_2(self.mat)
        self.update_grid()

        if status != "GAME NOT OVER":
            new_records = game_history.generate_report(count_up, count_down, count_left, count_right, status, max_value_on_gameboard)
            if new_records:
                status += "\n\nNEW RECORDS MADE:\n"
                for record, value_of_record in new_records:
                    status += record + ":" + str(value_of_record) + "\n"
            self.status_label.config(text=status)
            self.root_window.unbind("<Key>")
        else:
            self.status_label.config(text="")
        return