import json


def load_settings(data):
    '''Save new settings
    :param data: volume and difficulty value
    :type data: dict
    :returns: None
    '''
    with open('settings.txt', 'w') as settings_file:
        json.dump(data, settings_file)


def read_settings():
    '''Get settings information
    :returns: volume and difficulty value
    :rtype: dict
    '''
    with open('settings.txt') as settings_file:
        settings = json.load(settings_file)
    return settings
