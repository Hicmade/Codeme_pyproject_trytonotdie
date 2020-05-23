import sqlite3


def execute_script(cursor, script_file):
    with open(script_file, encoding='utf-8') as f:
        query = f.read()
    cursor.executescript(query)


if __name__ == '__main__':
    conn = sqlite3.connect('./usables/game_data.db')
    cursor = conn.cursor()

    execute_script(cursor, './sql/drop_tables.sql')
    execute_script(cursor, './sql/character_set_init.sql')
    execute_script(cursor, './sql/game_save_init.sql')
    execute_script(cursor, './sql/users_init.sql')

    conn.commit()

    conn.close()
