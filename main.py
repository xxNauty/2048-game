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

def unhide_main_menu(window):
    root_window.deiconify()
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
    game_window.protocol("WM_DELETE_WINDOW", lambda: unhide_main_menu(game_window))
    game_window.focus_force() #ustawienie fokusa na nowo otwartym oknie


def history_of_games():
    history_window = tk.Toplevel(root_window)

    history_window.title("Last 10 played games")
    history_window.geometry(get_geometry(history_window, 440, 600))

    history_content = game_history.GameHistory(master=history_window)
    history_content.pack(fill="both", expand=True)

    root_window.iconify()
    history_window.protocol("WM_DELETE_WINDOW", lambda: unhide_main_menu(history_window))

def settings():
    settings_window = tk.Toplevel(root_window)

    settings_window.title("Choose the level of game")
    settings_window.geometry(get_geometry(settings_window, 440, 600))

    with open("game_settings.json", "r") as file:
        data = json.loads(file.read())
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
                command=lambda id_=identifier: (mark_as_checked(data, id_), unhide_main_menu(settings_window)),
                state="disabled" if data[identifier]['checked'] else "normal"
            )
            level_label.pack(pady=10)
        file.close()

        root_window.iconify()
        settings_window.protocol("WM_DELETE_WINDOW", lambda: unhide_main_menu(settings_window))

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