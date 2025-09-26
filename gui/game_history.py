import tkinter as tk
import os
import json

GAME_HISTORY_FILE = "logs/"

class GameHistory(tk.Frame):
    def __init__(self, master = None, main_menu_frame = None):
        super().__init__(master)
        self.main_menu_frame = main_menu_frame
        self.get_data()

    def get_data(self):
        background = tk.Frame(self)
        background.pack(fill="both", expand=True)

        header = tk.Label(
            master=background,
            text="Last 10 games played",
            font=("Verdana", 20, "bold"),
            justify="center",
        )
        header.pack(pady=5)

        games = tk.Frame(
            master=background,
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
                justify="center",
                font=("Verdana", 16, "normal")
            )
            no_games_label.pack(pady=10)
            return

        for file in files:
            cell = tk.Button(
                master=games,
                text=file[:-5],
                justify="center",
                font=("Verdana", 16, "normal"),
                width=19,
                command=lambda f=file: self.get_details(f)
            )
            cell.grid(pady=5, padx=5)

        return_button = tk.Button(
            master=background,
            text="Return to Main menu",
            font=("Verdana", 20, "normal"),
            command=lambda: self.main_menu_frame.tkraise()
        )
        return_button.pack()

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
