import os
import tkinter as tk
from dotenv import load_dotenv
from gui import game, game_history

load_dotenv()

root = tk.Tk()
root.title("2048 game")
root.geometry("440x600")

container = tk.Frame(root)
container.pack(fill="both", expand=True)

main_menu_frame = tk.Frame(container)
main_menu_frame.grid(row=0, column=0, sticky="nsew")

game_frame = tk.Frame(container)
game_frame.grid(row=0, column=0, sticky="nsew")
game_content = game.Game(master=game_frame, root_window=root)
game_content.pack(fill="both", expand=True)
root.bind("<Key>", game_content.key_down)

game_history_frame = tk.Frame(container)
game_history_frame.grid(row=0, column=0, sticky="nsew")
game_history_content = game_history.GameHistory(master=game_history_frame, main_menu_frame=main_menu_frame)
game_history_content.pack(fill="both", expand=True)


title_label = tk.Label(
    master=main_menu_frame,
    text="2048",
    font=("Verdana", 30, "bold"),
    justify="center"
)
title_label.pack(pady=10)

def play_game():
    root.geometry(f"{int(os.getenv("GAMEBOARD_SIZE")) * 110}x{int(os.getenv("GAMEBOARD_SIZE")) * 110}")
    game_frame.tkraise()

play_button = tk.Button(
    master=main_menu_frame,
    text="New game",
    font=("Verdana", 20, "normal"),
    justify="center",
    width=10,
    command=play_game
)
play_button.pack(pady=10)

def history_of_games():
    game_history_frame.tkraise()

history_button = tk.Button(
    master=main_menu_frame,
    text="Last games",
    font=("Verdana", 20, "normal"),
    justify="center",
    width=10,
    command=history_of_games
)
history_button.pack(pady=10)

settings_button = tk.Button(
    master=main_menu_frame,
    text="Settings",
    font=("Verdana", 20, "normal"),
    justify="center",
    width=10,
    state="disabled"
)
settings_button.pack(pady=10)

def quit_game():
    root.destroy()

end_button = tk.Button(
    master=main_menu_frame,
    text="Quit game",
    font=("Verdana", 20, "normal"),
    justify="center",
    width=10,
    command=quit_game
)

end_button.pack(pady=10)
records_frame = tk.Frame(container)

records_frame.grid(row=0, column=0, sticky="nsew")
results_frame = tk.Frame(container)

results_frame.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    main_menu_frame.tkraise()
    root.mainloop()