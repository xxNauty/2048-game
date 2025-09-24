import tkinter as tk

from gui import game, game_history, main_menu, records, results

root = tk.Tk()
root.title("2048 game")
root.geometry("440x600")

container = tk.Frame(root)
container.pack(fill="both", expand=True)

game_frame = tk.Frame(container)
game_frame.grid(row=0, column=0, sticky="nsew")
game_content = game.Game(master=game_frame, root_window=root)
game_content.pack(fill="both", expand=True)
root.bind("<Key>", game_content.key_down)

game_history_frame = tk.Frame(container)
game_history_frame.grid(row=0, column=0, sticky="nsew")
game_history_content = game_history.GameHistory(master=game_history_frame)
game_history_content.pack(fill="both", expand=True)

main_menu_frame = tk.Frame(container)
main_menu_frame.grid(row=0, column=0, sticky="nsew")

records_frame = tk.Frame(container)
records_frame.grid(row=0, column=0, sticky="nsew")

results_frame = tk.Frame(container)
results_frame.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    # game_history_frame.tkraise()
    game_frame.tkraise()
    root.mainloop()