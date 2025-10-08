import datetime
import tkinter as tk
import os
import json

from backend import common
from dotenv import load_dotenv

load_dotenv()

class GameHistory(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.game_history_path = os.getenv("GAME_HISTORY_PATH")
        self.get_data()


    def get_data(self):
        background = tk.Frame(self)
        background.pack(fill="both", expand=True)

        header_label = tk.Label(
            master=background,
            text="Last 10 games played",
            font=("Verdana", 20, "bold"),
            justify="center",
        )
        header_label.pack(pady=5)

        games_widget = tk.Frame(
            master=background,
        )
        games_widget.pack(pady=5)

        files = [file for file in os.listdir(self.game_history_path) if os.path.isfile(os.path.join(self.game_history_path, file))]

        #ignorowanie nadmiarowych plików
        for ignore_file in ["example.json", "records.json", ".gitignore"]:
            if ignore_file in files:
                files.remove(ignore_file)

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
                text=datetime.datetime.strptime(file[:-5], os.getenv("DATE_FORMAT_FOR_FILENAMES")).strftime(os.getenv("DATE_FORMAT_NORMAL")),
                justify="center",
                font=("Verdana", 16, "normal"),
                width=19,
                command=lambda f=file: self.get_details(f)
            )
            game_button.grid(pady=5, padx=5)

    def get_details(self, filename):
        try:
            with open(self.game_history_path + filename) as file:
                data = file.read()
                data = json.loads(data)

                details_window = tk.Toplevel()
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

                for i, (k, v) in enumerate(data.items()):
                    data_key = k.replace("_", " ").capitalize()
                    tk.Label(details_widget, text=data_key, font=("Verdana", 15, "bold"), borderwidth=2, relief="solid",
                             width=14).grid(row=i, column=0, sticky='w')
                    tk.Label(details_widget, text=v, font=("Verdana", 15, "normal"), borderwidth=2, relief="solid",
                             width=16).grid(row=i, column=1, sticky='w')
        except FileNotFoundError:
            error_window = tk.Toplevel(self)
            error_window.title("An error occurred")
            error_window.geometry(common.get_geometry(error_window, 440, 600))

            error_title = tk.Label(
                master=error_window,
                text=f"File {filename} does not exist"
            )
            error_title.pack()
        except json.JSONDecodeError:
            error_window = tk.Toplevel(self)
            error_window.title("An error occurred")
            error_window.geometry(common.get_geometry(error_window, 440, 600))

            error_title = tk.Label(
                master=error_window,
                text=f"Something went wrong with the file {filename}"
            )
            error_title.pack()
