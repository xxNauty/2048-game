import os
import json

from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def update_records(game_identifier, count_up, count_down, count_left, count_right, max_value_on_gameboard):
    total_moves = count_up + count_down + count_left + count_right
    current_date = datetime.now().strftime(os.getenv("DATE_FORMAT"))
    records_path = "logs/records.json"

    updated = []

    with open(records_path, "r+") as file:
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

            file.seek(0) # ustawienie kursora na początek pliku
            file.truncate() # wyczyszczenie zawartości pliku, w przeciwnym razie mogą pojawić się problemy przy różnicy długości plików
            json.dump(data, file, indent=4)
        file.close()

    return updated