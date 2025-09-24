import tkinter as tk

from gui import game, game_history, main_menu, records, results

root = tk.Tk()
root.title("2048 game")
root.geometry("440x600")

game_frame = tk.Frame(root)
game_frame.grid(row=0, column=0)
game_content = game.Game(master=game_frame)
game_content.pack(fill="both", expand=True)
root.bind("<Key>", game_content.key_down)

# game_history_frame = tk.Frame(root)
# game_history_frame.grid(row=0, column=0)
# game_history_content = game_history.GameHistory(master=game_history_frame)
# game_history_content.pack(fill="both", expand=True)

main_menu_frame = tk.Frame(root)
records_frame = tk.Frame(root)
results_frame = tk.Frame(root)

if __name__ == "__main__":
    game_frame.tkraise()
    root.mainloop()