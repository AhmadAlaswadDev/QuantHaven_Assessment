import json
from pathlib import Path

DATA_DIR = Path("data")


def read_json(file_name: str) -> list:
    file_path = DATA_DIR / file_name

    if not file_path.exists():
        return []

    with file_path.open("r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def write_json(file_name: str, data: list) -> None:
    DATA_DIR.mkdir(exist_ok=True)

    file_path = DATA_DIR / file_name

    with file_path.open("w") as file:
        json.dump(data, file, indent=2)


def append_json(
    file_name: str,
    item: dict,
    should_be_unique: bool = False,
    unique_key: str = "id"
) -> None:
    data = read_json(file_name)
    if should_be_unique:
        if any(entry.get(unique_key) == item.get(unique_key) for entry in data):
            raise ValueError(f"Duplicate entry for key: {unique_key}")

    data.append(item)
    write_json(file_name, data)

def exists(file_name: str, key: str, value) -> bool:
    data = read_json(file_name)
    return any(entry.get(key) == value for entry in data)