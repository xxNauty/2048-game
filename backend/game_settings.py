import os
import json

import game_status

from dotenv import load_dotenv
from json import JSONDecodeError
from gui import exception_handler

load_dotenv()


def read_settings():
    try:
        with open(os.getenv("GAME_SETTINGS_PATH"), "r") as file:
            data = json.loads(file.read())
            return data
    except FileNotFoundError:
        exception_handler.handle_file_not_found_error(os.getenv("GAME_SETTINGS_PATH"))
    except JSONDecodeError:
        exception_handler.handle_JSON_decode_error()

def mark_as_checked(data, element):
    try:
        with open(os.getenv("GAME_SETTINGS_PATH"), "w") as file:
            for index in range(len(data)):
                data[str(index + 1)]['checked'] = False

            data[element]['checked'] = True

            game_status.current_settings['size'] = data[element]['size']
            game_status.current_settings['end_value'] = data[element]['end_val']

            file.seek(0)
            file.truncate()

            json.dump(data, file, indent=4)

    except FileNotFoundError:
        exception_handler.handle_file_not_found_error(os.getenv("GAME_SETTINGS_PATH"))
    except JSONDecodeError:
        exception_handler.handle_JSON_decode_error()