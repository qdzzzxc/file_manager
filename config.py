import os
import json

work_dir = os.path.join(os.getcwd(), "directory")


def load_json():
    with open("config.json", "r") as config_file:
        loaded_config = json.load(config_file)

    return list(loaded_config.values())


def save_json(bg_color, active_color, selected_color):
    config = {
        "bg_color": bg_color,
        "active_color": active_color,
        "selected_color": selected_color,
    }

    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)
