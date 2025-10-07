import json
import os
import sys
import tkinter as tk
from gui import game, game_history
from dotenv import load_dotenv

load_dotenv()

def kill_app():
    sys.exit()

# ustawia okno na środku ekranu, koordynaty liczone są od lewego górnego rogu
def get_geometry(root_window, width, height):
    if width < 440:
        width = 440

    if height < 600:
        height = 600

    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    return f"{width}x{height}+{x}+{y}"

def unhide_main_menu(root, window):
    root.deiconify()
    window.destroy()

def mark_as_checked(data, element):
    with open("game_settings.json", "w") as file:

        for index in range(len(data)):
            data[str(index + 1)]['checked'] = False

        data[element]['checked'] = True

        file.seek(0)
        file.truncate()

        json.dump(data, file)
        print(data, element, sep="\n")
        file.close()

def play_game():
    game_window = tk.Toplevel(root_window)

    game_window.title("2048 Game")

    game_content = game.Game(master=game_window, root_window=root_window)
    game_content.pack(fill="both", expand=True)

    game_window.geometry(get_geometry(game_window, game_content.size * 110, game_content.size * 110))

    game_window.bind("<Key>", game_content.key_down)

    root_window.iconify()
    game_window.protocol("WM_DELETE_WINDOW", lambda: unhide_main_menu(root_window, game_window))
    game_window.focus_force() #ustawienie fokusa na nowo otwartym oknie


def history_of_games():
    history_window = tk.Toplevel(root_window)

    history_window.title("Last 10 played games")
    history_window.geometry(get_geometry(history_window, 440, 600))

    history_content = game_history.GameHistory(master=history_window)
    history_content.pack(fill="both", expand=True)

    root_window.iconify()
    history_window.protocol("WM_DELETE_WINDOW", lambda: unhide_main_menu(root_window, history_window))

def settings():
    settings_window = tk.Toplevel(root_window)

    settings_window.title("Choose the level of game")
    settings_window.geometry(get_geometry(settings_window, 440, 600))

    with open("game_settings.json", "r") as file:
        data = json.loads(file.read())
        for element in range(len(data)):
            identifier = str(element + 1)
            level_label = tk.Button(
                master=settings_window,
                text=data[identifier],
                font=("Verdana", 12, "normal"),
                justify="center",
                width=40,
                command=lambda id_=identifier: (mark_as_checked(data, id_), unhide_main_menu(root_window, settings_window)),
                state="disabled" if data[identifier]['checked'] else "normal"
            )
            level_label.pack(pady=10)
        file.close()

        root_window.iconify()
        settings_window.protocol("WM_DELETE_WINDOW", lambda: unhide_main_menu(root_window, settings_window))

def records():
    records_window = tk.Toplevel(root_window)

    records_window.title("Your personal records")
    records_window.geometry(get_geometry(records_window, 440, 600))

    records_frame = tk.Frame(
        master=records_window,
    )
    records_frame.pack(pady=10)

    for i, (level_name, level_file) in enumerate([("(3x3->64)   ", "3_64"), ("(4x4->1024)", "4_1024"),
                                                  ("(4x4->2048)", "4_2048"), ("(5x5->2048)", "5_2048"),
                                                  ("(6x6->4096)", "6_4096")]):
        level_button = tk.Button(
            master=records_frame,
            height=1,
            font=("Verdana", 20, "normal"),
            text=f"Level {i + 1} {level_name}",
            command=lambda level_file_=level_file, records_window_=records_window: records_details(level_file_, records_window_)
        )
        level_button.pack(pady=10)

    root_window.iconify()
    records_window.protocol("WM_DELETE_WINDOW", lambda: unhide_main_menu(root_window, records_window))

def records_details(file_name, previous_window):
    records_details_window = tk.Toplevel(previous_window)

    records_details_window.title("Your personal records")
    records_details_window.geometry(get_geometry(records_details_window, 440, 600))

    with open("records/" + file_name + ".json") as file:
        record_details = json.loads(file.read())
        print(file_name)

        tk.Label(
            records_details_window,
            text="Your personal records for level xxx",
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
        records_details_window.protocol("WM_DELETE_WINDOW", lambda: unhide_main_menu(previous_window, records_details_window))


if __name__ == "__main__":
    root_window = tk.Tk()
    root_window.title("2048 Game")
    root_window.geometry(get_geometry(root_window, 440, 600))

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
        command=records
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