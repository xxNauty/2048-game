import json
import sys
import tkinter as tk
import backend.logic as logic
import backend.moves as moves
import backend.state as state
import backend.game_history as game_history
from main import get_geometry

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

def unhide_main_menu(root, window):
    root.deiconify()
    window.destroy()

class Game(tk.Frame):
    def __init__(self, master=None, root_window=None):
        super().__init__(master)
        self.root_window = root_window
        self.size = 4
        self.end_value = 2048
        self.grid_cells = []
        self.read_settings()
        self.grid()
        self.init_grid()
        self.mat = logic.start_game(self.size)
        self.update_grid()

    def read_settings(self):
        with open("game_settings.json", "r") as file:
            data = json.loads(file.read())
            for i in range(len(data)):
                i = str(i + 1)
                if data[i]['checked']:
                    self.size = data[i]['size']
                    self.end_value = data[i]['end_val']

    def init_grid(self):
        background = tk.Frame(self, bg="#bbada0", width=self.size * 110, height=self.size * 110)
        background.pack(anchor="center")
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
                    relief="raised",
                    borderwidth=5
                )
                t.grid()
                row.append(t)
            self.grid_cells.append(row)

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

        moves.set_size(self.size)

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

        status, max_value_on_gameboard = state.get_current_state(self.mat, self.size, self.end_value)
        if status == "GAME NOT OVER" and moved:
            logic.add_new_2(self.mat, self.size)
        self.update_grid()

        if status != "GAME NOT OVER":
            new_records, output_file_name = game_history.generate_report(count_up, count_down, count_left, count_right, status, max_value_on_gameboard)
            self.end_game_window(status, new_records, output_file_name)
            self.master.unbind("<Key>")


    def end_game_window(self, status, records, output_file_name):
        end_game_window = tk.Toplevel()
        end_game_window.title("Game over")
        end_game_window.geometry(get_geometry(end_game_window, 440, 600))
        status_formatted = ""
        if status == "WIN":
            status_formatted = "You win!"
        elif status == "LOST":
            status_formatted = "You lost!"


        game_result_status_label = tk.Label(
            master=end_game_window,
            text=status_formatted,
            font=("Verdana", 20, "bold"),
            justify="center"
        )
        game_result_status_label.pack(pady=5)

        if records:
            records_label = tk.Label(
                master=end_game_window,
                text="New records made!",
                font=("Verdana", 16, "normal"),
                justify="center"
            )
            records_label.pack(pady=5)

        quit_button = tk.Button(
            master=end_game_window,
            text="Quit game",
            font=("Verdana", 20, "normal"),
            justify="center",
            width=10,
            command=lambda: sys.exit()
        )
        quit_button.pack(pady=10)

        view_details_button = tk.Button(
            master=end_game_window,
            text="Statistics",
            font=("Verdana", 20, "normal"),
            justify="center",
            width=10,
            command=lambda: self.after_game_statistics(output_file_name, end_game_window)
        )
        view_details_button.pack()
        end_game_window.protocol("WM_DELETE_WINDOW", lambda: sys.exit())

    def after_game_statistics(self, filename, parent_window):
        with open(filename, "r") as file:
            data = file.read()
            data = json.loads(data)

            parent_window.iconify()

            after_game_statistics_window = tk.Toplevel()
            after_game_statistics_window.title("Details of the game")
            after_game_statistics_window.geometry(get_geometry(after_game_statistics_window, 440, 600))

            title_label = tk.Label(
                master=after_game_statistics_window,
                text="Details of the game",
                font=("Verdana", 16, "normal"),
                justify="center"
            )
            title_label.pack()

            details_widget = tk.Frame(
                master=after_game_statistics_window,
                width=440,
                height=440,
            )
            details_widget.pack(pady=10)

            for i, (k, v) in enumerate(data.items()):
                data_key = k.replace("_", " ").capitalize()
                tk.Label(details_widget, text=data_key, font=("Verdana", 15, "bold"), borderwidth=2, relief="solid", width=14).grid(row=i, column=0, sticky='w')
                tk.Label(details_widget, text=v, font=("Verdana", 15, "normal"), borderwidth=2, relief="solid", width=16).grid(row=i, column=1, sticky='w')

            after_game_statistics_window.protocol("WM_DELETE_WINDOW",  lambda: unhide_main_menu(parent_window, after_game_statistics_window))