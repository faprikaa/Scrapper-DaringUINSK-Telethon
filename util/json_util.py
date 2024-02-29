import json


def load_saved_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)


def get_saved_data_by_post_id(post_id):
    datas = load_saved_data()
    result = datas.get(str(post_id))
    return result
