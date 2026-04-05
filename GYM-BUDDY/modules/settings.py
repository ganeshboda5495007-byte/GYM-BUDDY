import json
import os

SETTINGS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "settings.json"
)

DEFAULT_SETTINGS = {
    "username": "User",
    "height": 170,
    "weight": 70,
    "age": 25,
    "gender": "male",
    "activity_level": "moderate",
    "theme": "light",
    "notifications": True,
    "units": "metric",
    "daily_goal": 30,
    "sound_effects": True,
}


def load_settings():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                return {**DEFAULT_SETTINGS, **json.load(f)}
        return DEFAULT_SETTINGS.copy()
    except:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    try:
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        return True
    except:
        return False


def get_settings():
    return load_settings()


def update_settings(new_settings):
    current = load_settings()
    current.update(new_settings)
    if save_settings(current):
        return current
    return None


def reset_settings():
    if save_settings(DEFAULT_SETTINGS):
        return DEFAULT_SETTINGS.copy()
    return None
