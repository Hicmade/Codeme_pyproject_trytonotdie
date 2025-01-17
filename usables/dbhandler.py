import sqlite3


class GameDatabase:

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
        conn = sqlite3.connect('./usables/game_data.db')
        c = conn.cursor()
        query = """
        SELECT * FROM GameSave WHERE ID = :ID
        """
        gameid = {'ID': game_id}
        try:
            c.execute(query, gameid)
            conn.commit()

            values = c.fetchall()
            result = dict(zip([c[0] for c in c.description], values[0]))
        except sqlite3.OperationalError:
            print("Operational error occured")
            result = "0"
        finally:
            conn.close()

        return result

    @staticmethod
    def input_character_set(chs, game_id):
        conn = sqlite3.connect('./usables/game_data.db')
        c = conn.cursor()
        query = """
        INSERT INTO CharacterSet VALUES (NULL, :GameID, :Ch_name, :Ch_occupation, :Ch_HP)
        """

        for x in chs:
            x.update(game_id)

        c.executemany(query, chs)
        conn.commit()

        conn.close()

    @staticmethod
    def get_character_set(game_id):
        conn = sqlite3.connect('./usables/game_data.db')
        c = conn.cursor()
        query = """
        SELECT * FROM CharacterSet WHERE GameID = :GameID
        """
        gameid = {'GameID': game_id}
        c.execute(query, gameid)
        conn.commit()

        list_of_values = c.fetchall()
        result = []
        for x in list_of_values:
            my_dict = dict(zip([c[0] for c in c.description], x))
            result.append(my_dict)

        conn.close()

        return result

    @staticmethod
    def update_character_set(chs):
        conn = sqlite3.connect('./usables/game_data.db')
        c = conn.cursor()
        query = """
        UPDATE CharacterSet SET CH_HP = :Ch_HP WHERE GAMEID = :GameID AND CH_NO = :Ch_no
        """

        c.executemany(query, chs)
        conn.commit()

        conn.close()

    @staticmethod
    def update_gamedata(data):

        conn = sqlite3.connect('./usables/game_data.db')
        c = conn.cursor()
        query = """
        UPDATE GameSave SET DAY = :day, FOOD_SUPL = :food_supl, HERB_SUPL = :herb_supl, HUTS = :huts, TEMP = :temp, 
        RAIN = :rain, RAIN_TXT = :rain_txt, WIND = :wind, 
        WIND_TXT = :wind_txt WHERE ID = :ID
        """

        c.executemany(query, (data,))
        conn.commit()

        conn.close()

    @staticmethod
    def save_game(data):
        conn = sqlite3.connect('./usables/game_data.db')
        c = conn.cursor()
        query = """
                SELECT * FROM Users WHERE User_id = :user_id AND User_pass = :user_pass
                """
        c.execute(query, data)
        conn.commit()
        res = c.fetchone()

        if res is None:
            query = """
            INSERT INTO Users VALUES (NULL, :user_id, :user_pass, :game_id)
            """
            c.execute(query, data)
            conn.commit()
        else:
            query = """
            UPDATE Users SET GAME_ID = :game_id WHERE USER_ID = :user_id AND USER_PASS = :user_pass
            """
            c.execute(query, data)
            conn.commit()

        conn.close()

    @staticmethod
    def load_game(data):
        conn = sqlite3.connect('./usables/game_data.db')
        c = conn.cursor()
        # query = """
        #         SELECT Game_id FROM Users WHERE User_id = :user_id AND User_pass = :user_pass
        #         """
        query = """
                SELECT Game_id FROM Users WHERE User_id = :user_id
                """
        c.execute(query, data)
        conn.commit()
        res = c.fetchone()

        if res is None:
            result = "0"
        else:
            result = res[0]

        conn.close()

        return result


if __name__ == "__main__":
    data = {"user_id": "b1",
            "user_pass": "p1",
            }

    r = GameDatabase.load_game(data)
    print(r)
