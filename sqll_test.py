from unittest.mock import *
from sqll import set_score_database, get_score_database
import pytest
import sqlite3
from Exceptions import *


def test_get_score_database():
    difficulty_list = ["Normal", "Hard", "Hardcore"]
    for difficulty in difficulty_list:
        sqlite3.connect = Mock()
        get_score_database(difficulty)
        sqlite3.connect.assert_called_with('scoreboard.db')


def test_exc_get_score_database():
    with pytest.raises(DifficultyError):
        get_score_database("Easy")


@patch('sqlite3.connect')
def test_1_set_score_database(mocksql):
    mock_cursor = mocksql.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = ("gg", 5)
    set_score_database("gg", 10, "Normal")
    mock_cursor.execute.assert_called_with('UPDATE Normal SET score="10" WHERE name="gg";')


@patch('sqlite3.connect')
def test_2_set_score_database(mocksql):
    mock_cursor = mocksql.return_value.cursor.return_value
    mock_cursor.fetchone.side_effect = [None, (4,)]
    set_score_database("gg", 10, "Normal")
    mock_cursor.execute.assert_called_with('INSERT INTO Normal(name, score) VALUES ("gg", "10");')


@patch('sqlite3.connect')
def test_3_set_score_database(mocksql):
    mock_cursor = mocksql.return_value.cursor.return_value
    mock_cursor.fetchone.side_effect = [None, (10,), (12,)]
    set_score_database("gg", 10, "Normal")
    mock_cursor.execute.assert_called_with('SELECT MIN(score) FROM Normal;')


@patch('sqlite3.connect')
def test_4_set_score_database(mocksql):
    mock_cursor = mocksql.return_value.cursor.return_value
    mock_cursor.fetchone.side_effect = [None, (10,), (7,), ("darling", 7)]
    set_score_database("gg", 10, "Normal")
    mock_cursor.execute.assert_called_with('INSERT INTO Normal(name, score) VALUES ("gg", "10");')


def test_exc_1_set_score_database():
    with pytest.raises(DifficultyError):
        set_score_database("darling", 23, "Impossible")


def test_exc_2_set_score_database():
    with pytest.raises(NegativeScoreError):
        set_score_database("darling", -3, "Hard")


def test_exc_3_set_score_database():
    with pytest.raises(OverflowError):
        set_score_database("VeryLongName", 4, "Hard")


def test_exc_4_set_score_database():
    with pytest.raises(WrongNameSyntaxError):
        set_score_database("Bun2Desy", 4, "Hard")
