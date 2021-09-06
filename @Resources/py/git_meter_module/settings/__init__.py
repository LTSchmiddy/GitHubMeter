# __all__

import sys
import os
import json


settings_path = "settings.json"

default_settings = {
    "github": {
        "user-token": None,
        "display-count": 5,
        "update-interval-min": 5
    },
    "local": {
        "paths": [],
        "search-depth": 3,
        "display-count": 5,
        "git-path": None,
        "update-interval-min": 1
    }
}

current = default_settings.copy()


def load_settings():
    global current
    current = default_settings.copy()

    def recursive_load_list(main: list, loaded: list):
        for i in range(0, max(len(main), len(loaded))):
            # Found in both:
            if i < len(main) and i < len(loaded):
                if isinstance(loaded[i], dict):
                    recursive_load_dict(main[i], loaded[i])
                elif isinstance(loaded[i], list):
                    recursive_load_list(main[i], loaded[i])
                else:
                    main[i] = loaded[i]
            # Found in main only:
            elif i < len(loaded):
                main.append(loaded[i])


    def recursive_load_dict(main: dict, loaded: dict):
        new_update_dict = {}
        for key, value in main.items():
            if not (key in loaded):
                continue
            if isinstance(value, dict):
                recursive_load_dict(value, loaded[key])
            elif isinstance(value, list):
                recursive_load_list(value, loaded[key])
            else:
                new_update_dict[key] = loaded[key]

        main.update(new_update_dict)

    # load preexistent settings file
    if os.path.exists(settings_path) and os.path.isfile(settings_path):
        try:
            imported_settings = json.load(open(settings_path, "r"))
            # current.update(imported_settings)
            recursive_load_dict(current, imported_settings)
        except json.decoder.JSONDecodeError as e:
            print (f"CRITICAL ERROR IN LOADING SETTINGS: {e}", fg='red')
            print ("Using default settings...", fg='yellow')

    # settings file not found
    else:
        save_settings()


def save_settings():
    global current
    json.dump(current, open(settings_path, "w"), indent=4)

from .setting_ref import SettingRef