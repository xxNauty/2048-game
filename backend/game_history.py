import json
import uuid
import os

import backend.records as records

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def generate_report(count_up, count_down, count_left, count_right, status, max_value_on_gameboard):
    remove_old_reports()
    game_identifier = str(uuid.uuid4()).split("-")[0]

    date_of_game = datetime.now()
    total_moves = count_up + count_down + count_left + count_right

    data = {
        "game_identifier": game_identifier,
        "date_of_game": date_of_game.strftime(os.getenv("DATE_FORMAT_NORMAL")),
        "total_moves": total_moves,
        "left_moves": count_left,
        "right_moves": count_right,
        "up_moves": count_up,
        "down_moves": count_down,
        "game_result": status,
        "highest_number": max_value_on_gameboard
    }

    new_records = records.update_records(game_identifier, count_up, count_down, count_left, count_right, max_value_on_gameboard)

    file_name = "logs/" + date_of_game.strftime(os.getenv("DATE_FORMAT_FOR_FILENAMES")) + ".json"

    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)
        file.close()

    return new_records, file_name

def remove_old_reports():
    files = [file for file in os.listdir("logs") if os.path.isfile(os.path.join("logs", file)) and file not in ["example.json", "records.json", ".gitignore"]]
    files.sort(reverse=True)
    for file in files[7:]:
        os.remove(os.path.join("logs", file))