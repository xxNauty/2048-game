import os
import json
import tkinter as tk
import backend.logic as logic
import backend.moves as moves
import backend.state as state
import backend.game_history as game_history
from dotenv import load_dotenv

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

load_dotenv()

class Game(tk.Frame):
    def __init__(self, master=None, root_window=None):
        super().__init__(master)
        self.root_window = root_window
        self.grid()
        self.size = int(os.getenv("GAMEBOARD_SIZE"))
        self.grid_cells = []
        self.init_grid()
        self.mat = logic.start_game()
        self.update_grid()

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
            new_records, output_file_name = game_history.generate_report(count_up, count_down, count_left, count_right, status, max_value_on_gameboard)
            self.end_game_window(status, new_records, output_file_name)
            self.root_window.unbind("<Key>")


    def end_game_window(self, status, records, output_file_name):
        window = tk.Tk()
        window.title("Game over")
        window.geometry("440x600")
        status_formatted = ""
        if status == "WIN":
            status_formatted = "You win!"
        elif status == "LOST":
            status_formatted = "You lost!"


        game_result_status = tk.Label(
            master=window,
            text=status_formatted,
            font=("Verdana", 20, "bold"),
            justify="center"
        )
        game_result_status.pack(pady=5)

        if records:
            records_label = tk.Label(
                master=window,
                text="New records made!",
                font=("Verdana", 16, "normal"),
                justify="center"
            )
            records_label.pack(pady=5)

        quit_button = tk.Button(
            master=window,
            text="Quit game",
            font=("Verdana", 20, "normal"),
            justify="center",
            width=10,
            command=lambda: self.quit_game(window)
        )
        quit_button.pack(pady=10)

        view_details_button = tk.Button(
            master=window,
            text="Statistics",
            font=("Verdana", 20, "normal"),
            justify="center",
            width=10,
            command=lambda: self.after_game_statistics(output_file_name)
        )
        view_details_button.pack()

    def after_game_statistics(self, filename):
        with open(filename, "r") as file:
            data = file.read()
            data = json.loads(data)

            window = tk.Tk()
            window.title("Details of the game")
            window.geometry("440x600")

            title_widget = tk.Label(
                master=window,
                text="Details of the game",
                font=("Verdana", 16, "normal"),
                justify="center"
            )
            title_widget.pack()

            details_widget = tk.Label(
                master=window,
                text=self.format_text(data),
                justify="left",
                font=("Verdana", 12, "normal")
            )
            details_widget.pack()

    def quit_game(self, window):
        window.destroy()
        self.root_window.destroy()

    @staticmethod
    def format_text(details):
        output = ""
        for key, value in details.items():
            output += f"{key.capitalize()}: {value}\n"
        return output

