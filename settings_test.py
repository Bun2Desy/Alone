import pytest
from exceptions import InvalidDictionaryError, DifficultyError, VolumeError
from settings import load_settings, read_settings
from unittest.mock import patch


@patch('json.dump')
def test_load_settings(mockjson):
    data = {"volume": 0.5, "difficulty": "Hard"}
    load_settings(data)
    mockjson.assert_called()


def test_exc_1_load_settings():
    with pytest.raises(InvalidDictionaryError):
        data = {"difficulty": "Hard"}
        load_settings(data)


def test_exc_2_load_settings():
    with pytest.raises(InvalidDictionaryError):
        data = {"volume": 0.5}
        load_settings(data)


def test_exc_3_load_settings():
    with pytest.raises(VolumeError):
        data = {"volume": 1.4, "difficulty": "Hard"}
        load_settings(data)


def test_exc_4_load_settings():
    with pytest.raises(DifficultyError):
        data = {"volume": 0.4, "difficulty": "Very Hard"}
        load_settings(data)


@patch('json.load')
def test_read_settings(mockjson):
    mockjson.return_value = {"volume": 0.24, "difficulty": "Normal"}
    result = read_settings()
    assert result == {"volume": 0.24, "difficulty": "Normal"}


@patch('json.load')
def test_exc_1_read_settings(mockjson):
    with pytest.raises(InvalidDictionaryError):
        mockjson.return_value = {"difficulty": "Hardcore"}
        read_settings()


@patch('json.load')
def test_exc_2_read_settings(mockjson):
    with pytest.raises(InvalidDictionaryError):
        mockjson.return_value = {"volume": 0.89}
        read_settings()


@patch('json.load')
def test_exc_3_read_settings(mockjson):
    with pytest.raises(VolumeError):
        mockjson.return_value = {"volume": 24, "difficulty": "Hard"}
        read_settings()


@patch('json.load')
def test_exc_4_read_settings(mockjson):
    with pytest.raises(DifficultyError):
        mockjson.return_value = {"volume": 0.4, "difficulty": "Easy"}
        read_settings()
