import tkinter as tk
import os
import json

GAME_HISTORY_FILE = "logs/"

class GameHistory(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.get_data()

    def get_data(self):
        background = tk.Frame(
            self,
            bg="#bbada0",
        )
        background.pack(fill="both", expand=True)

        header = tk.Label(
            master=background,
            text="Last 10 games played",
            font=("Verdana", 14, "bold"),
            bg="#bbada0",
            justify="center",
        )
        header.pack(pady=5)

        games = tk.Frame(
            master=background,
            bg="#bbada0",
        )
        games.pack(pady=5)

        files = [file for file in os.listdir(GAME_HISTORY_FILE) if os.path.isfile(os.path.join(GAME_HISTORY_FILE, file))]

        #ignorowanie nadmiarowych plików
        for ignore_file in ["example.json", "records.json", ".gitignore"]:
            if ignore_file in files:
                files.remove(ignore_file)

        if not files:
            no_games_label = tk.Label(
                master=games,
                text="No game history available.",
                bg="#bbada0",
                justify="center",
                font=("Verdana", 12, "normal")
            )
            no_games_label.pack(pady=10)
            return

        for file in files:
            cell = tk.Button(
                master=games,
                text=file[:-5],
                bg="#9f9388",
                justify="center",
                font=("Verdana", 12, "normal"),
                width=16,
                height=1,
                relief="raised",
                borderwidth=5,
                command=lambda f=file: self.get_details(f)
            )
            cell.grid(pady=5, padx=5)

    def get_details(self, filename):
        with open(GAME_HISTORY_FILE + filename) as file:
            details = file.read()
            details = json.loads(details)

            window = tk.Tk()
            window.title("Details of game")
            window.geometry("440x440")
            text_label = tk.Label(
                window,
                text=f"Details of game: {details['game_identifier']}",
                justify="center",
                font=("Verdana", 20, "bold")
            )
            text_label.pack()

            text_widget = tk.Label(
                window,
                text=self.format_text(details),
                justify="left",
                font=("Verdana", 12, "normal")
            )
            text_widget.pack()



    @staticmethod
    def clear_window(root: tk.Tk):
        for widget in root.winfo_children():
            widget.destroy()

    @staticmethod
    def format_text(details):
        output = ""
        for key, value in details.items():
            output += f"{key.capitalize()}: {value}\n"
        return output
