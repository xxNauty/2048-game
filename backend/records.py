import os
import json

from dotenv import load_dotenv
from datetime import datetime
from json import JSONDecodeError
from gui import exception_handler

load_dotenv()

def update_records(game_identifier, game_settings, count_up, count_down, count_left, count_right, max_value_on_gameboard):
    total_moves = count_up + count_down + count_left + count_right
    current_date = datetime.now().strftime(os.getenv("DATE_FORMAT_NORMAL"))

    updated = []
    try:
        with open(os.getenv("RECORDS_PATH") + f"{game_settings[0]}_{game_settings[1]}.json", "r+") as file:
            if file.read() == '':
                data = {
                    "last_update": current_date,
                    "moves_up": {
                        "record": count_up,
                        "last_update": current_date,
                        "updated_by": game_identifier
                    },
                    "moves_down": {
                        "record": count_down,
                        "last_update": current_date,
                        "updated_by": game_identifier
                    },
                    "moves_left": {
                        "record": count_left,
                        "last_update": current_date,
                        "updated_by": game_identifier
                    },
                    "moves_right": {
                        "record": count_right,
                        "last_update": current_date,
                        "updated_by": game_identifier
                    },
                    "total_moves": {
                        "record": total_moves,
                        "last_update": current_date,
                        "updated_by": game_identifier
                    },
                    "max_value_on_gameboard": {
                        "record": max_value_on_gameboard,
                        "last_update": current_date,
                        "updated_by": game_identifier
                    },
                }
                json.dump(data, file, indent=4)
            else:
                file.seek(0)
                data = json.load(file)

                if data['moves_up']['record'] > count_up:
                    data['moves_up']['record'] = count_up
                    data['moves_up']['last_update'] = current_date
                    data['moves_up']['updated_by'] = game_identifier
                    updated.append(("moves_up", count_up))

                if data['moves_down']['record'] > count_down:
                    data['moves_down']['record'] = count_down
                    data['moves_down']['last_update'] = current_date
                    data['moves_down']['updated_by'] = game_identifier
                    updated.append(("moves_down", count_down))

                if data['moves_left']['record'] > count_left:
                    data['moves_left']['record'] = count_left
                    data['moves_left']['last_update'] = current_date
                    data['moves_left']['updated_by'] = game_identifier
                    updated.append(("moves_left", count_left))

                if data['moves_right']['record'] > count_right:
                    data['moves_right']['record'] = count_right
                    data['moves_right']['last_update'] = current_date
                    data['moves_right']['updated_by'] = game_identifier
                    updated.append(("moves_right", count_right))

                if data['total_moves']['record'] > total_moves:
                    data['total_moves']['record'] = total_moves
                    data['total_moves']['last_update'] = current_date
                    data['total_moves']['updated_by'] = game_identifier
                    updated.append(("total_moves", total_moves))

                if data['max_value_on_gameboard']['record'] < max_value_on_gameboard:
                    data['max_value_on_gameboard']['record'] = max_value_on_gameboard
                    data['max_value_on_gameboard']['last_update'] = current_date
                    data['max_value_on_gameboard']['updated_by'] = game_identifier
                    updated.append(("max_value_on_gameboard", max_value_on_gameboard))

                if updated:
                    data['last_update'] = current_date

                file.seek(0)
                file.truncate()
                json.dump(data, file, indent=4)
    except FileNotFoundError:
        exception_handler.handle_file_not_found_error(f"{game_settings[0]}_{game_settings[1]}.json")
    except JSONDecodeError:
        exception_handler.handle_JSON_decode_error()

    return updated

def read_records(file_name):
    try:
        with open(os.getenv("RECORDS_PATH") + file_name + ".json") as file:
            record_details = json.loads(file.read())
            return record_details
    except FileNotFoundError:
        exception_handler.handle_file_not_found_error(file_name + ".json")
    except JSONDecodeError:
        exception_handler.handle_JSON_decode_error()