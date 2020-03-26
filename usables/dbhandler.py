import sqlite3


class GameDatabase:

    @staticmethod
    def create_db():
        conn = sqlite3.connect('game_data.db')
        c = conn.cursor()
        c.execute("CREATE TABLE MainSave (ID int NOT NULL, character_num, day, food_supl, herb_supl, huts, temp, rain, "
                  "rain_txt, wind, wind_txt, ch1_n, ch1_o, ch1_hp, ch2_n, ch2_o, ch2_hp, ch3_n, ch3_o, ch3_hp, "
                  "ch4_n, ch4_o, ch4_hp, user_id, user_pass)")
        c.execute("CREATE UNIQUE INDEX id ON MainSave (ID)")
        c.execute("CREATE UNIQUE INDEX usr ON MainSave (user_id)")
        conn.commit()
        conn.close()


    @staticmethod
    def input_gamedata(data):
        conn = sqlite3.connect('game_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO MainSave VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,"
                  " ?, ?)", data)
        conn.commit()
        conn.close()


    @staticmethod
    def test_data():
        my_keys = ["ID", "character_num", "day", "food_supl", "herb_supl", "huts", "temp", "rain",
                  "rain_txt", "wind", "wind_txt", "ch1_n", "ch1_o", "ch1_hp", "ch2_n", "ch2_o", "ch2_hp", "ch3_n",
                  "ch3_o", "ch3_hp", "ch4_n", "ch4_o", "ch4_hp", "user_id", "user_pass"]
        my_values = (1, 1, 1, 3, 3, 3, 20, 2, "Rain", 2, "Windy", "Character1", "Doc", 100, "Character2", "Ranger",
                     90, "Character3", "Engineer", 80, "Character4", "Influencer", 70, "Bartek", "bartek")
        output = dict(zip(my_keys, my_values))
        return my_values

    @staticmethod
    def delete_table():
        conn = sqlite3.connect('game_data.db')
        c = conn.cursor()
        c.execute("DROP TABLE MainSave")
        conn.commit()
        conn.close()

    @staticmethod
    def create_index():
        conn = sqlite3.connect('game_data.db')
        c = conn.cursor()
        c.execute("CREATE UNIQUE INDEX id ON MainSave (ID)")
        c.execute("CREATE UNIQUE INDEX usr ON MainSave (user_id)")
        conn.commit()
        conn.close()


if __name__ == "__main__":
    data = GameDatabase.test_data()
    GameDatabase.input_gamedata(data)

    # GameDatabase.delete_table()

    # GameDatabase.create_db()

    # GameDatabase.create_index()