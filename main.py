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

def play_game():
    game_window = tk.Toplevel()

    game_window.title("2048 Game")
    game_window.geometry(get_geometry(game_window, int(os.getenv("GAMEBOARD_SIZE")) * 110, int(os.getenv("GAMEBOARD_SIZE")) * 110))

    game_content = game.Game(master=game_window, root_window=root_window)
    game_content.pack(fill="both", expand=True)

    game_window.bind("<Key>", game_content.key_down)

    root_window.iconify()
    game_window.protocol("WM_DELETE_WINDOW", lambda: unhide_main_menu(game_window))
    game_window.focus_force() #ustawienie fokusa na nowo otwartym oknie


def history_of_games():
    history_window = tk.Toplevel()

    history_window.title("Last 10 played games")
    history_window.geometry(get_geometry(history_window, 440, 600))

    history_content = game_history.GameHistory(master=history_window)
    history_content.pack(fill="both", expand=True)

    root_window.iconify()
    history_window.protocol("WM_DELETE_WINDOW", lambda: unhide_main_menu(history_window))

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
        state="disabled"
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