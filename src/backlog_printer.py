from pathlib import Path
import json
import os

STORAGE = "../data/back_log"

def get_backlog_info():
    storage_path = Path(STORAGE)
    all_data = []

    for file in storage_path.glob("*.json"):
        try:
            with file.open("r") as f:
                data = json.load(f)

                all_data.append(data)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Failed to read or parse {file.name}: {e}")

    return all_data

def get_list():
    storage_path = Path(STORAGE)
    all_names = []
    count = 1
    for file in storage_path.glob("*.json"):
        if count >= 25:
            break
        try:
            with file.open("r") as f:
                data = json.load(f)

                all_names.append(data["title"])
        except (json.JSONDecodeError, OSError) as e:
            print(f"Failed to read or parse {file.name}: {e}")
        count += 1

    return all_names

def deleted_log(game):
    game = game.replace(' ', '') + ".json"

    os.remove(STORAGE + '/' + game)