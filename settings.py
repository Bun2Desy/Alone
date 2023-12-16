import json

def load_settings(data):
    with open('settings.txt', 'w') as settings_file:
        json.dump(data, settings_file)

def read_settings():
    with open('settings.txt') as settings_file:
        settings = json.load(settings_file)
    return settings
