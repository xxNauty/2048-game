import json
import sys
import tkinter as tk

import game_status

from backend import logic, moves, state, game_history, common

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
    4096: ("#edc000", "#f9f6f2")
}

class Game(tk.Frame):
    def __init__(self, master=None, root_window=None):
        super().__init__(master)
        self.root_window = root_window
        self.master = master
        self.grid_cells = []
        self.game_board = logic.start_game()
        logic.add_new_2(self.game_board)
        self.grid()
        self.window()
        self.update_grid()

    def window(self):
        game_window = tk.Frame(self)
        game_window.pack(anchor="center")
        for i in range(game_status.current_settings['size']):
            row = []
            for j in range(game_status.current_settings['size']):
                cell = tk.Frame(
                    game_window,
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
        for i in range(game_status.current_settings['size']):
            for j in range(game_status.current_settings['size']):
                value = self.game_board[i][j]
                color_bg, color_fg = COLORS.get(value, ("#3c3a32", "#f9f6f2"))
                label = self.grid_cells[i][j]
                label.config(text=str(value) if value else "",bg=color_bg, fg=color_fg)
        self.update_idletasks()

    def key_down(self, event):
        key = event.keysym

        if key in ["Up", "w", "W"]:
            game_status.moves_count['up'] += 1
            self.game_board, moved = moves.move_up(self.game_board)

        elif key in ["Down", "s", "S"]:
            game_status.moves_count['down'] += 1
            self.game_board, moved = moves.move_down(self.game_board)

        elif key in ["Left", "a", "A"]:
            game_status.moves_count['left'] += 1
            self.game_board, moved = moves.move_left(self.game_board)

        elif key in ["Right", "d", "D"]:
            game_status.moves_count['right'] += 1
            self.game_board, moved = moves.move_right(self.game_board)

        else:
            return

        status, max_value_on_gameboard = state.get_current_state(self.game_board)
        if status == "GAME NOT OVER" and moved:
            logic.add_new_2(self.game_board)
        self.update_grid()

        if status != "GAME NOT OVER":
            new_records, output_file_name = game_history.generate_report(
                (game_status.current_settings['size'], game_status.current_settings['end_value']),
                game_status.moves_count['up'],
                game_status.moves_count['down'],
                game_status.moves_count['left'],
                game_status.moves_count['right'],
                status,
                max_value_on_gameboard
            )
            self.end_game_window(status, new_records, output_file_name)
            self.master.unbind("<Key>")


    def end_game_window(self, status, records, output_file_name):
        end_game_window = tk.Toplevel()
        end_game_window.title("Game over")
        end_game_window.geometry(common.get_geometry(end_game_window, 440, 600))
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
        try:
            with open(filename, "r") as file:
                data = file.read()
                data = json.loads(data)

                parent_window.iconify()

                after_game_statistics_window = tk.Toplevel()
                after_game_statistics_window.title("Details of the game")
                after_game_statistics_window.geometry(common.get_geometry(after_game_statistics_window, 440, 600))

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

                after_game_statistics_window.protocol("WM_DELETE_WINDOW",  lambda: common.unhide_previous_window(parent_window, after_game_statistics_window))
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass