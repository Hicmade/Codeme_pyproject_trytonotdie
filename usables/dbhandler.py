import sqlite3


class GameDatabase:

    # @staticmethod
    # def create_db():
    #     conn = sqlite3.connect('game_data.db')
    #     c = conn.cursor()
    #     c.execute("CREATE TABLE MainSave (ID int NOT NULL, character_num, day, food_supl, herb_supl, huts, temp, rain, "
    #               "rain_txt, wind, wind_txt, ch1_n, ch1_o, ch1_hp, ch2_n, ch2_o, ch2_hp, ch3_n, ch3_o, ch3_hp, "
    #               "ch4_n, ch4_o, ch4_hp, user_id, user_pass)")
    #     c.execute("CREATE UNIQUE INDEX id ON MainSave (ID)")
    #     c.execute("CREATE UNIQUE INDEX usr ON MainSave (user_id)")
    #     conn.commit()
    #     conn.close()


    @staticmethod
    def input_gamedata(data):
        conn = sqlite3.connect('./usables/game_data.db')
        c = conn.cursor()
        query = """
        INSERT INTO GameSave VALUES (NULL, :day, :food_supl, :herb_supl, :huts, :temp, :rain, :rain_txt, :wind, 
        :wind_txt, NULL, NULL)
        """
        c.execute(query, data)
        game_id = c.lastrowid

        conn.commit()
        conn.close()

        return game_id


    @staticmethod
    def get_gamedata(game_id):
        conn = sqlite3.connect('game_data.db')
        c = conn.cursor()
        query = """
        SELECT * FROM GameSave WHERE ID = ?
        """
        c.execute(query, (game_id,))
        conn.commit()

        result = c.fetchall()

        conn.close()

        return result

    @staticmethod
    def input_character_set(chs, game_id):
        conn = sqlite3.connect('./usables/game_data.db')
        c = conn.cursor()
        query = """
        INSERT INTO CharacterSet VALUES (:GameID, :Ch_name, :Ch_occupation, :Ch_HP)
        """

        for x in chs:
            x.update(game_id)

        c.executemany(query, chs)
        conn.commit()

        conn.close()


    @staticmethod
    def get_character_set(game_id):
        conn = sqlite3.connect('game_data.db')
        c = conn.cursor()
        query = """
        SELECT * FROM CharacterSet WHERE GameID = ?
        """
        c.execute(query, (game_id,))
        conn.commit()

        result = c.fetchall()

        conn.close()

        return result

if __name__ == "__main__":
    GameDatabase.get_character_set(3)
