import sqlite3


def set_score_database(name, score, difficulty):
    create_table(difficulty)

    scoreboard_connect = sqlite3.connect('scoreboard.db')
    cursor = scoreboard_connect.cursor()

    cursor.execute(f'SELECT * FROM {difficulty} WHERE name="{name}";')
    response = cursor.fetchone()
    if response != None:
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
    create_table(difficulty)

    scoreboard_connect = sqlite3.connect('scoreboard.db')
    cursor = scoreboard_connect.cursor()

    cursor.execute(f'SELECT * FROM {difficulty} ORDER BY score DESC;')
    return cursor.fetchall()

def create_table(table_name):
    scoreboard_connect = sqlite3.connect('scoreboard.db')
    cursor = scoreboard_connect.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name}(
            name TEXT,
            score INT);
        ''')
    scoreboard_connect.commit()
    scoreboard_connect.close()

print(get_score_database("Hard"))