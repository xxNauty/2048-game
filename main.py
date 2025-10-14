import sys
import tkinter as tk

import game_status

from backend import common, logic, game_settings
from gui import (
    game as game_gui,
    game_history as game_history_gui,
    game_settings as game_settings_gui,
    game_records as game_records_gui
)
from dotenv import load_dotenv

load_dotenv()

def window_play_game():
    game_window = tk.Toplevel(root_window)

    game_window.title("2048 Game")

    game_content = game_gui.Game(master=game_window, root_window=root_window)
    game_content.pack(fill="both", expand=True)

    game_window.geometry(common.get_geometry(game_window, game_status.current_settings['size'] * 110, game_status.current_settings['size'] * 110))

    game_window.bind("<Key>", game_content.key_down)

    root_window.iconify()
    game_window.protocol("WM_DELETE_WINDOW", lambda: common.unhide_previous_window(root_window, game_window))
    game_window.focus_force()


def window_history_of_games():
    history_window = tk.Toplevel(root_window)

    history_window.title("Last 10 played games")
    history_window.geometry(common.get_geometry(history_window, 440, 600))

    history_content = game_history_gui.GameHistory(master=history_window)
    history_content.pack(fill="both", expand=True)

    root_window.iconify()
    history_window.protocol("WM_DELETE_WINDOW", lambda: common.unhide_previous_window(root_window, history_window))

def window_settings():
    settings_window = tk.Toplevel(root_window)

    settings_window.title("Choose the level of game")
    settings_window.geometry(common.get_geometry(settings_window, 440, 600))

    settings_content = game_settings_gui.GameSettings(master=settings_window, root_window=root_window)
    settings_content.pack(fill="both", expand=True)

    root_window.iconify()
    settings_window.protocol("WM_DELETE_WINDOW", lambda: common.unhide_previous_window(root_window, settings_window))

def window_game_records():
    records_window = tk.Toplevel(root_window)

    records_window.title("Your personal records")
    records_window.geometry(common.get_geometry(records_window, 440, 600))

    records_content = game_records_gui.GameRecords(master=records_window, root_window=root_window)
    records_content.pack(fill="both", expand=True)

    root_window.iconify()
    records_window.protocol("WM_DELETE_WINDOW", lambda: common.unhide_previous_window(root_window, records_window))

if __name__ == "__main__":
    settings = game_settings.read_settings()
    for i in range(len(settings)):
        i = str(i + 1)
        if settings[i]['checked']:
            game_status.current_settings['size'] = settings[i]['size']
            game_status.current_settings['end_value'] = settings[i]['end_val']

    root_window = tk.Tk()
    root_window.title("2048 Game")
    root_window.geometry(common.get_geometry(root_window, 440, 600))

    title_label = tk.Label(
        master=root_window,
        text="2048",
        font=("Verdana", 30, "bold"),
        justify="center"
    )
    title_label.pack(pady=10)

    play_button = tk.Button(
        master=root_window,
        text="New game",
        font=("Verdana", 20, "normal"),
        justify="center",
        width=10,
        command=window_play_game
    )
    play_button.pack(pady=10)

    history_button = tk.Button(
        master=root_window,
        text="Last games",
        font=("Verdana", 20, "normal"),
        justify="center",
        width=10,
        command=window_history_of_games
    )
    history_button.pack(pady=10)

    settings_button = tk.Button(
        master=root_window,
        text="Settings",
        font=("Verdana", 20, "normal"),
        justify="center",
        width=10,
        command=window_settings
    )
    settings_button.pack(pady=10)

    records_button = tk.Button(
        master=root_window,
        text="Records",
        font=("Verdana", 20, "normal"),
        justify="center",
        width=10,
        command=window_game_records
    )
    records_button.pack()

    end_button = tk.Button(
        master=root_window,
        text="Quit game",
        font=("Verdana", 20, "normal"),
        justify="center",
        width=10,
        command=lambda: sys.exit()
    )
    end_button.pack(pady=10)

    root_window.mainloop()