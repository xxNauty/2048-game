import os
import json

from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

script_path = Path(__file__).resolve()
directory = script_path.parent

def reset():
    for file in directory.iterdir():
        if file.is_file() and file != script_path:
            with open(file, 'r+') as file_data:
                content = file_data.read()
                json_content = json.loads(content)
                current_date = datetime.now().strftime(os.getenv("DATE_FORMAT_NORMAL"))
                for element in json_content:
                    if "moves_" in element:
                        json_content[element]['record'] = 999
                        json_content[element]['last_update'] = current_date
                        json_content[element]['updated_by'] = "record not set"
                    elif element == "total_moves":
                        json_content[element]['record'] = 3996
                        json_content[element]['last_update'] = current_date
                        json_content[element]['updated_by'] = "record not set"
                    elif element == "max_value_on_gameboard":
                        json_content[element]['record'] = 0
                        json_content[element]['last_update'] = current_date
                        json_content[element]['updated_by'] = "record not set"
                json_content['last_update'] = current_date
                file_data.seek(0)
                file_data.truncate()
                json.dump(json_content, file_data, indent=4)
                file_data.close()

if __name__ == "__main__":
    reset()