import json
from Exceptions import *


def load_settings(data):
    '''Save new settings
    :param data: volume and difficulty value
    :type data: dict
    :returns: None
    '''
    if data.get("volume") is None or data.get("difficulty") is None:
        raise InvalidDictionaryError
    if data.get("volume") not in [i / 100 for i in range(101)]:
        raise VolumeError
    if data.get("difficulty") not in ["Normal", "Hard", "Hardcore"]:
        raise DifficultyError
    with open('settings.txt', 'w') as settings_file:
        json.dump(data, settings_file)


def read_settings():
    '''Get settings information
    :returns: volume and difficulty value
    :rtype: dict
    '''
    with open('settings.txt') as settings_file:
        settings = json.load(settings_file)
    if settings.get("volume") is None or settings.get("difficulty") is None:
        raise InvalidDictionaryError
    if settings.get("volume") not in [i / 100 for i in range(101)]:
        raise VolumeError
    if settings.get("difficulty") not in ["Normal", "Hard", "Hardcore"]:
        raise DifficultyError
    return settings
