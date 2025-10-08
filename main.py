import sys
import tkinter as tk

from backend import common, game_settings, records
from gui import game, game_history
from dotenv import load_dotenv


load_dotenv()

def play_game():
    game_window = tk.Toplevel(root_window)

    game_window.title("2048 Game")

    game_content = game.Game(master=game_window, root_window=root_window)
    game_content.pack(fill="both", expand=True)

    game_window.geometry(common.get_geometry(game_window, game_content.size * 110, game_content.size * 110))

    game_window.bind("<Key>", game_content.key_down)

    root_window.iconify()
    game_window.protocol("WM_DELETE_WINDOW", lambda: common.unhide_previous_window(root_window, game_window))
    game_window.focus_force()


def history_of_games():
    history_window = tk.Toplevel(root_window)

    history_window.title("Last 10 played games")
    history_window.geometry(common.get_geometry(history_window, 440, 600))

    history_content = game_history.GameHistory(master=history_window)
    history_content.pack(fill="both", expand=True)

    root_window.iconify()
    history_window.protocol("WM_DELETE_WINDOW", lambda: common.unhide_previous_window(root_window, history_window))

def settings():
    settings_window = tk.Toplevel(root_window)

    settings_window.title("Choose the level of game")
    settings_window.geometry(common.get_geometry(settings_window, 440, 600))

    data = game_settings.read_settings()
    for element in range(len(data)):
        identifier = str(element + 1)
        formatted_text = "Size: " + str(data[identifier]['size']) + " | End value: " + str(data[identifier]['end_val'])
        if data[identifier]['end_val'] == 64:
            formatted_text += "   "
        level_label = tk.Button(
            master=settings_window,
            text=formatted_text,
            font=("Verdana", 12, "normal"),
            justify="center",
            width=40,
            command=lambda id_=identifier: (game_settings.mark_as_checked(data, id_), common.unhide_previous_window(root_window, settings_window)),
            state="disabled" if data[identifier]['checked'] else "normal"
        )
        level_label.pack(pady=10)

    root_window.iconify()
    settings_window.protocol("WM_DELETE_WINDOW", lambda: common.unhide_previous_window(root_window, settings_window))

def game_records():
    records_window = tk.Toplevel(root_window)

    records_window.title("Your personal records")
    records_window.geometry(common.get_geometry(records_window, 440, 600))

    records_frame = tk.Frame(
        master=records_window,
    )
    records_frame.pack(pady=10)

    for i, (level_name, level_file) in enumerate([
        ("(3x3->64)   ", "3_64"),
        ("(4x4->1024)", "4_1024"),
        ("(4x4->2048)", "4_2048"),
        ("(5x5->2048)", "5_2048"),
        ("(6x6->4096)", "6_4096")
    ]):
        level_button = tk.Button(
            master=records_frame,
            height=1,
            font=("Verdana", 20, "normal"),
            text=f"Level {i + 1} {level_name}",
            command=lambda level_ = i, level_file_ = level_file, records_window_ = records_window: records_details(level_, level_file_, records_window_)
        )
        level_button.pack(pady=10)

    root_window.iconify()
    records_window.protocol("WM_DELETE_WINDOW", lambda: common.unhide_previous_window(root_window, records_window))

def records_details(level, file_name, previous_window):
    records_details_window = tk.Toplevel(previous_window)

    records_details_window.title("Your personal records")
    records_details_window.geometry(common.get_geometry(records_details_window, 450, 600))

    record_details = records.read_records(file_name)

    tk.Label(
        records_details_window,
        text=f"Your personal records for level {level + 1}",
        font=("Verdana", 16, "normal")
    ).grid(row=0, column=0, columnspan=4, pady=(0, 10))
    tk.Label(
        records_details_window,
        text=f"Last Update: {record_details['last_update']}",
        font=("Verdana", 10, "normal")
    ).grid(row=1, column=0, columnspan=4, pady=(0, 20))

    headers = ["Stat", "Record", "Last Update", "Updated By"]
    for i, h in enumerate(headers):
        tk.Label(records_details_window, text=h, font=("Arial", 10, "bold")).grid(row=2, column=i, padx=8, sticky="w")

    rows = [
        ("Moves Up", record_details["moves_up"]),
        ("Moves Down", record_details["moves_down"]),
        ("Moves Left", record_details["moves_left"]),
        ("Moves Right", record_details["moves_right"]),
        ("Total Moves", record_details["total_moves"]),
        ("Max Value on Gameboard", record_details["max_value_on_gameboard"])
    ]

    for idx, (label, stats) in enumerate(rows, start=3):
        tk.Label(records_details_window, text=label, font=("Verdana", 9), justify="center").grid(row=idx, column=0, sticky="w")
        tk.Label(records_details_window, text=stats["record"], font=("Verdana", 9), justify="center").grid(row=idx, column=1, sticky="w")
        tk.Label(records_details_window, text=stats["last_update"], font=("Verdana", 9), justify="center").grid(row=idx, column=2, sticky="w")
        tk.Label(records_details_window, text=stats["updated_by"], font=("Verdana", 9), justify="center").grid(row=idx, column=3, sticky="w")

    previous_window.iconify()
    records_details_window.protocol("WM_DELETE_WINDOW", lambda: common.unhide_previous_window(previous_window, records_details_window))

if __name__ == "__main__":
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
        command=play_game
    )
    play_button.pack(pady=10)

    history_button = tk.Button(
        master=root_window,
        text="Last games",
        font=("Verdana", 20, "normal"),
        justify="center",
        width=10,
        command=history_of_games
    )
    history_button.pack(pady=10)

    settings_button = tk.Button(
        master=root_window,
        text="Settings",
        font=("Verdana", 20, "normal"),
        justify="center",
        width=10,
        command=settings
    )
    settings_button.pack(pady=10)

    records_button = tk.Button(
        master=root_window,
        text="Records",
        font=("Verdana", 20, "normal"),
        justify="center",
        width=10,
        command=game_records
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