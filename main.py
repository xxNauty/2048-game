import os
import sys
import tkinter as tk
from gui import game, game_history
from dotenv import load_dotenv

load_dotenv()

def kill_app():
    sys.exit()

root = tk.Tk()

root.title("2048 Game")
root.geometry("440x600")

container = tk.Frame(root)
container.pack(fill="both", expand=True)

if __name__ == "__main__":
    def unhide_main_menu(window):
        root.deiconify()
        window.destroy()

    def play_game():
        game_window = tk.Toplevel()

        game_window.title("2048 Game")
        game_window.geometry(f"{int(os.getenv("GAMEBOARD_SIZE")) * 110}x{int(os.getenv("GAMEBOARD_SIZE")) * 110}")

        game_content = game.Game(master=game_window, root_window=root)
        game_content.pack(fill="both", expand=True)

        game_window.bind("<Key>", game_content.key_down)

        root.iconify()
        game_window.protocol("WM_DELETE_WINDOW", lambda: unhide_main_menu(game_window))


    def history_of_games():
        history_window = tk.Toplevel()

        history_window.title("Last 10 played games")
        history_window.geometry("440x600")

        history_content = game_history.GameHistory(master=history_window)
        history_content.pack(fill="both", expand=True)

        root.iconify()
        history_window.protocol("WM_DELETE_WINDOW", lambda: unhide_main_menu(history_window))

    def quit_game():
        root.destroy()


    title_label = tk.Label(
        master=container,
        text="2048",
        font=("Verdana", 30, "bold"),
        justify="center"
    )
    title_label.pack(pady=10)

    play_button = tk.Button(
        master=container,
        text="New game",
        font=("Verdana", 20, "normal"),
        justify="center",
        width=10,
        command=play_game
    )
    play_button.pack(pady=10)

    history_button = tk.Button(
        master=container,
        text="Last games",
        font=("Verdana", 20, "normal"),
        justify="center",
        width=10,
        command=history_of_games
    )
    history_button.pack(pady=10)

    settings_button = tk.Button(
        master=container,
        text="Settings",
        font=("Verdana", 20, "normal"),
        justify="center",
        width=10,
        state="disabled"
    )
    settings_button.pack(pady=10)

    end_button = tk.Button(
        master=container,
        text="Quit game",
        font=("Verdana", 20, "normal"),
        justify="center",
        width=10,
        command=quit_game
    )
    end_button.pack(pady=10)

    root.mainloop()