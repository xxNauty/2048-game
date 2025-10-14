import tkinter as tk

from backend import game_settings, common

class GameSettings(tk.Frame):
    def __init__(self, master = None, root_window = None):
        super().__init__(master)
        self.root_window = root_window
        self.master = master
        self.settings = game_settings.read_settings()
        self.window()

    def window(self):
        settings_window = tk.Frame(self)
        settings_window.pack(anchor="center")

        data = self.settings
        for element in range(len(data)):
            identifier = str(element + 1)
            formatted_text = "Size: " + str(data[identifier]['size']) + " | End value: " + str(
                data[identifier]['end_val'])
            if data[identifier]['end_val'] == 64:
                formatted_text += "   "
            level_label = tk.Button(
                master=settings_window,
                text=formatted_text,
                font=("Verdana", 12, "normal"),
                justify="center",
                width=40,
                command=lambda id_=identifier: (
                    game_settings.mark_as_checked(data, id_),
                    common.unhide_previous_window(self.root_window, self.master)
                ),
                state="disabled" if data[identifier]['checked'] else "normal"
            )
            level_label.pack(pady=10)