import tkinter as tk

from backend import records, common

LEVELS = [
        ("(3x3->64)   ", "3_64"),
        ("(4x4->1024)", "4_1024"),
        ("(4x4->2048)", "4_2048"),
        ("(5x5->2048)", "5_2048"),
        ("(6x6->4096)", "6_4096")
]

class GameRecords(tk.Frame):
    def __init__(self, master = None, root_window = None):
        super().__init__(master)
        self.root_window = root_window,
        self.master = master
        self.window()

    def window(self):
        records_window = tk.Frame(self)
        records_window.pack(anchor="center")

        for i, (level_name, level_file_name) in enumerate(LEVELS):
            level_button = tk.Button(
                master=records_window,
                height=1,
                font=("Verdana", 20, "normal"),
                text=f"Level {i + 1} {level_name}",
                command=lambda
                    level_=i,
                    level_file_=level_file_name:
                self.records_details(level_, level_file_)
            )
            level_button.pack(pady=10)

    def records_details(self, level, file_name):
        records_details_window = tk.Toplevel(self.master)

        records_details_window.title("Your personal records")
        records_details_window.geometry(common.get_geometry(records_details_window, 450, 600))

        record_details = records.read_records(file_name)

        tk.Label(
            records_details_window,
            text=f"Your personal records for level {level + 1}",
            font=("Verdana", 16, "normal")
        ).grid(row=0, column=0, columnspan=4, pady=(0, 10))
        tk.Label(
            records_details_window,
            text=f"Last Update: {record_details['last_update']}",
            font=("Verdana", 10, "normal")
        ).grid(row=1, column=0, columnspan=4, pady=(0, 20))

        headers = ["Stat", "Record", "Last Update", "Updated By"]
        for i, h in enumerate(headers):
            tk.Label(
                records_details_window,
                text=h,
                font=("Arial", 10, "bold")
            ).grid(row=2, column=i, padx=8, sticky="w")

        rows = [
            ("Moves Up", record_details["moves_up"]),
            ("Moves Down", record_details["moves_down"]),
            ("Moves Left", record_details["moves_left"]),
            ("Moves Right", record_details["moves_right"]),
            ("Total Moves", record_details["total_moves"]),
            ("Max Value on Gameboard", record_details["max_value_on_gameboard"])
        ]

        for idx, (label, stats) in enumerate(rows, start=3):
            tk.Label(
                records_details_window,
                text=label,
                font=("Verdana", 9),
                justify="center"
            ).grid(row=idx, column=0, sticky="w")
            tk.Label(
                records_details_window,
                text=stats["record"],
                font=("Verdana", 9),
                justify="center"
            ).grid(row=idx, column=1, sticky="w")
            tk.Label(
                records_details_window,
                text=stats["last_update"],
                font=("Verdana", 9),
                justify="center"
            ).grid(row=idx, column=2, sticky="w")
            tk.Label(
                records_details_window,
                text=stats["updated_by"],
                font=("Verdana", 9),
                justify="center"
            ).grid(row=idx, column=3, sticky="w")

        self.master.iconify()

        records_details_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: common.unhide_previous_window(self.master, records_details_window)
        )
