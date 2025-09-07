import json

def save_to_json(filename, data):
    f = open(filename, "w")
    json.dump(data, f)
    f.close()

def load_from_json(filename):
    f = None
    try:
        f = open(filename, "r", encoding="utf-8")
        return json.load(f)
    except FileNotFoundError:
        return []
    finally:
        if f is not None:
            f.close()