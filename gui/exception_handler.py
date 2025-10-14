import tkinter as tk
from backend import common

def handle_file_not_found_error(filename):
    _handle(f"The file {filename} is missing")

def handle_JSON_decode_error():
    _handle(f"Something is wrong with the JSON structure in the file")

def _handle(error_message):
    error_window = tk.Tk()
    error_window.title("Something went wrong")
    error_window.geometry(common.get_geometry(error_window, 440, 600))

    title = tk.Label(
        error_window,
        text="An error occurred",
        font=("Verdana", 20, "normal")
    )
    title.pack(pady=10)

    explaination = tk.Label(
        error_window,
        text=error_message,
        font=("Verdana", 12, "normal"),
    )
    explaination.pack(pady=10)