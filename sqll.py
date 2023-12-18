import sqlite3
from Exceptions import *


def set_score_database(name, score, difficulty):
    '''Load new result in database
    :param name: hero name
    :type name: str
    :param score: hero score
    :type score: int
    :param difficulty: game difficulty
    :type difficulty: str
    :returns: None
    '''
    create_table(difficulty)

    if score < 0:
        raise NegativeScoreError
    if len(name) > 10:
        raise OverflowError
    if not name.isalpha():
        raise WrongNameSyntaxError

    scoreboard_connect = sqlite3.connect('scoreboard.db')
    cursor = scoreboard_connect.cursor()

    cursor.execute(f'SELECT * FROM {difficulty} WHERE name="{name}";')
    response = cursor.fetchone()
    if response is not None:
        if response[1] < score:
            cursor.execute(f'UPDATE {difficulty} SET score="{score}" WHERE name="{name}";')
    else:
        cursor.execute(f'SELECT COUNT(*) FROM {difficulty};')
        count = cursor.fetchone()
        if count[0] == 10:
            cursor.execute(f'SELECT MIN(score) FROM {difficulty};')
            min_score = cursor.fetchone()
            if score > min_score[0]:
                cursor.execute(f'SELECT * FROM {difficulty} WHERE score="{min_score[0]}";')
                min_name = cursor.fetchone()
                cursor.execute(f'DELETE FROM {difficulty} WHERE name="{min_name[0]}";')
                cursor.execute(f'INSERT INTO {difficulty}(name, score) VALUES ("{name}", "{score}");')
        else:
            cursor.execute(f'INSERT INTO {difficulty}(name, score) VALUES ("{name}", "{score}");')

    scoreboard_connect.commit()
    scoreboard_connect.close()


def get_score_database(difficulty):
    '''Get data from database
    :param difficulty: game difficulty
    :type difficulty: str
    :returns: data from database
    :rtype: list
    '''
    create_table(difficulty)

    scoreboard_connect = sqlite3.connect('scoreboard.db')
    cursor = scoreboard_connect.cursor()

    cursor.execute(f'SELECT * FROM {difficulty} ORDER BY score DESC;')
    return cursor.fetchall()


def create_table(table_name):
    '''Create table
    :param table_name: name of the table
    :type table_name: str
    :returns: None
    '''
    if table_name not in ["Normal", "Hard", "Hardcore"]:
        raise DifficultyError
    scoreboard_connect = sqlite3.connect('scoreboard.db')
    cursor = scoreboard_connect.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name}(
            name TEXT,
            score INT);
        ''')
    scoreboard_connect.commit()
    scoreboard_connect.close()
