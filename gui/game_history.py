import os
import tkinter as tk

from datetime import datetime
from dotenv import load_dotenv
from backend import common, game_history

load_dotenv()

class GameHistory(tk.Frame):
    def __init__(self, master = None, root_window = None):
        super().__init__(master)
        self.root_window = root_window
        self.master = master
        self.window()

    def window(self):
        history_window = tk.Frame(self)
        history_window.pack(anchor="center")

        header_label = tk.Label(
            master=self,
            text="Last 10 games played",
            font=("Verdana", 20, "bold"),
            justify="center"
        )
        header_label.pack(pady=5)

        games_widget = tk.Frame(master=self)
        games_widget.pack(pady=5)

        files = game_history.read_history_files()

        if not files:
            no_games_label = tk.Label(
                master=games_widget,
                text="No game history available.",
                justify="center",
                font=("Verdana", 16, "normal")
            )
            no_games_label.pack(pady=10)
            return

        for file in files:
            game_button = tk.Button(
                master=games_widget,
                text=datetime.strptime(
                    file[:-5],
                    os.getenv("DATE_FORMAT_FOR_FILENAMES")
                ).strftime(os.getenv("DATE_FORMAT_NORMAL")),
                justify="center",
                font=("Verdana", 16, "normal"),
                width=19,
                command=lambda file_=file: self.get_details(file_)
            )
            game_button.grid(pady=5, padx=5)

    def get_details(self, file_name):
        data = game_history.get_details(file_name)

        details_window = tk.Toplevel(self)
        details_window.title("Details of game")
        details_window.geometry(common.get_geometry(details_window, 440, 600))
        text_label = tk.Label(
            details_window,
            text=f"Details of game: {data['game_identifier']}",
            justify="center",
            font=("Verdana", 20, "bold")
        )
        text_label.pack()

        details_widget = tk.Frame(
            master=details_window,
            width=440,
            height=440,
        )
        details_widget.pack(pady=10)

        for i, (key, value) in enumerate(data.items()):
            key = key.replace("_", " ").capitalize()
            tk.Label(details_widget, text=key, font=("Verdana", 15, "bold"), borderwidth=2, relief="solid",
                     width=14).grid(row=i, column=0, sticky='w')
            tk.Label(details_widget, text=value, font=("Verdana", 15, "normal"), borderwidth=2, relief="solid",
                     width=16).grid(row=i, column=1, sticky='w')