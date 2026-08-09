from pathlib import Path
import json

def get_backlog_info():
    storage_path = Path("../data/back_log")
    all_data = []

    for file in storage_path.glob("*.json"):
        try:
            with file.open("r") as f:
                data = json.load(f)

                all_data.append(data)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Failed to read or parse {file.name}: {e}")

    print("done")
    print(all_data)
    return all_data

get_backlog_info()