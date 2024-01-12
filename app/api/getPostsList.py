import json

def get_posts_from_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            print("a")
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = []
    return data