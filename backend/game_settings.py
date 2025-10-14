import json

import game_status

from json import JSONDecodeError

def read_settings():
    try:
        with open("game_settings.json", "r") as file:
            data = json.loads(file.read())
            return data
    except FileNotFoundError:
        pass
    except JSONDecodeError:
        pass
    finally:
        file.close()

def mark_as_checked(data, element):
    try:
        with open("game_settings.json", "w") as file:
            for index in range(len(data)):
                data[str(index + 1)]['checked'] = False

            data[element]['checked'] = True

            game_status.current_settings['size'] = data[element]['size']
            game_status.current_settings['end_value'] = data[element]['end_val']

            file.seek(0)
            file.truncate()

            json.dump(data, file, indent=4)

            file.close()
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass
    finally:
        file.close()