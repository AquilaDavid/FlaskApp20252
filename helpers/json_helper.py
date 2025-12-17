import json

def read_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)