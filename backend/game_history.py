import json
import uuid
import os

from json import JSONDecodeError
from backend import records
from gui import exception_handler
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GAME_HISTORY_PATH = os.getenv("GAME_HISTORY_PATH")
IGNORED_FILES = ["example.json", ".gitignore"]

def generate_report(game_settings, count_up, count_down, count_left, count_right, status, max_value_on_gameboard):
    remove_old_reports()
    game_identifier = str(uuid.uuid4()).split("-")[0]

    date_of_game = datetime.now()
    total_moves = count_up + count_down + count_left + count_right

    data = {
        "game_identifier": game_identifier,
        "size of gameboard": f"{game_settings[0]}x{game_settings[0]}",
        "date_of_game": date_of_game.strftime(os.getenv("DATE_FORMAT_NORMAL")),
        "total_moves": total_moves,
        "left_moves": count_left,
        "right_moves": count_right,
        "up_moves": count_up,
        "down_moves": count_down,
        "game_result": status,
        "highest_number": max_value_on_gameboard
    }

    new_records = records.update_records(game_identifier, game_settings, count_up, count_down, count_left, count_right, max_value_on_gameboard)

    file_name = GAME_HISTORY_PATH + date_of_game.strftime(os.getenv("DATE_FORMAT_FOR_FILENAMES")) + f"-{game_settings[0]}x{game_settings[0]}" + ".json"

    with open(file_name, "w") as file:
        json.dump(data, file, indent=4) # indent=4 to prevent from making inline JSON

    return new_records, date_of_game.strftime(os.getenv("DATE_FORMAT_FOR_FILENAMES")) + ".json"

def remove_old_reports():
    files = [
        file
        for file in os.listdir(GAME_HISTORY_PATH)
        if os.path.isfile(os.path.join(GAME_HISTORY_PATH, file))
           and file not in IGNORED_FILES
    ]
    files.sort(reverse=True)
    for file in files[int(os.getenv("GAME_HISTORY_SIZE")):]:
        os.remove(os.path.join(GAME_HISTORY_PATH, file))

def read_history_files():
    files = [
        file
        for file in os.listdir(GAME_HISTORY_PATH)
        if os.path.isfile(os.path.join(GAME_HISTORY_PATH, file))
    ]

    for ignore_file in IGNORED_FILES:
        if ignore_file in files:
            files.remove(ignore_file)

    return files

def get_details(file_name):
    try:
        with open(GAME_HISTORY_PATH + file_name) as file:
            data = json.loads(file.read())
            return data
    except FileNotFoundError:
        exception_handler.handle_file_not_found_error(file_name)
    except JSONDecodeError:
        exception_handler.handle_JSON_decode_error()
