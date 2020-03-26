import random
import math


class GameControl:

    """
    howmany = 4
    character_occupation = ["doctor", "ranger", "engineer", "influencer"]
    character_set = {"ch1": None,
                     "ch2": None,
                     "ch3": None,
                     "ch4": None,}
    character_names = ["Glados", "Brajanusz", "Kira", "Calypso", "Drake", "Sasha"]
    character_surnames = ["McFly", "Croft", "Python", "Li", "Codeyou", "Grey"]
    names_set = []

    def default_character_set(self, co=character_occupation):
        i = 0
        for key, value in self.character_set.items():
            self.character_set[key] = co[i]
            i += 1
        return self.character_set

    def character_names(self, hm=howmany, chn=character_names, chs=character_surnames):
        name_keys = []
        for i in range(hm):
            name_keys.append("nam"+str(i+1))
            self.names_set.append(random.choice(chn)+" "+random.choice(chs))
        result = dict(zip(name_keys, self.names_set))
        return result
    """

    @staticmethod
    def get_initial_weather():
        init_weather = {
            'temp': 20,
            'rain': 'Clear sky',
            'wind': 'No'
        }

        return init_weather

    @staticmethod
    def get_weather(temp):
        max_change = 10
        min_temp = 0
        max_temp = 40
        rain_types = [
            {"rain_txt": "Clear sky", "rain": 0},
            {"rain_txt": "Rain", "rain": 2},
            {"rain_txt": "Heavy rain", "rain": 3}
        ]
        wind_types = [
            {"wind_txt": "No", "wind": 0},
            {"wind_txt": "Windy", "wind": 2},
            {"wind_txt": "Very windy", "wind": 3}
        ]

        calculated_temp = random.randint(temp-max_change, temp+max_change)
        if calculated_temp < min_temp:
            calculated_temp = min_temp
        elif calculated_temp > max_temp:
            calculated_temp = max_temp

        calculated_rain = random.choice(rain_types)
        calculated_wind = random.choice(wind_types)

        weather = {
            'temp': calculated_temp,
            'rain': calculated_rain['rain'],
            'wind': calculated_wind['wind'],
            'rain_txt': calculated_rain['rain_txt'],
            'wind_txt': calculated_wind['wind_txt']
        }

        return weather


class Character:
    t_doc = {
        'occupation': 'Doctor',
        'health_reg': 1.5,
        'health_los': 0.5,
        'heal': 4,
        'food_cons': 1,
        'hunt_eff': 1,
        'cold_proof': 1,
        'fix_constr': 1,
        'gather': 1,
        'HP': 100
    }

    t_ran = {
        'occupation': 'Ranger',
        'health_reg': 1.5,
        'health_los': 0.5,
        'heal': 2,
        'food_cons': 1.5,
        'hunt_eff': 4,
        'cold_proof': 0.5,
        'fix_constr': 2,
        'gather': 1,
        'HP': 100
    }

    t_eng = {
        'occupation': 'Engineer',
        'health_reg': 1,
        'health_los': 1,
        'heal': 1,
        'food_cons': 1.2,
        'hunt_eff': 2,
        'cold_proof': 1,
        'fix_constr': 4,
        'gather': 1,
        'HP': 100
    }

    t_inf = {
        'occupation': 'Influencer',
        'health_reg': 1.2,
        'health_los': 1.2,
        'heal': 1,
        'food_cons': 1,
        'hunt_eff': 1,
        'cold_proof': 1,
        'fix_constr': 1,
        'gather': 1,
        'HP': 100
    }
    this_char = {}

    _HP_max = 100
    character_names = ["Glados", "Brajanusz", "Kira", "Calypso", "Drake", "Sasha"]
    character_surnames = ["McFly", "Croft", "Python", "Li", "Codeyou", "Grey"]
    ch_name = None
    ch_occupation = None
    basic_food_gather = 5
    basic_herb_gather = 3
    basic_fix_construct = 0.25
    max_huts = 4

    def __init__(self, occup, hp=_HP_max):
        choices = {'doc': self.t_doc, 'ran': self.t_ran, 'eng': self.t_eng, 'inf': self.t_inf}
        self.this_char = choices.get(occup, "something went wrong")
        self.ch_occupation = self.this_char['occupation']
        self.this_char['HP'] = hp
        self.set_name()

    def set_name(self):
        self.ch_name = random.choice(self.character_names) + " " + random.choice(self.character_surnames)

    def bring_food(self):
        result = (random.randint(1, self.basic_food_gather)) * self.this_char['hunt_eff']
        return result

    def bring_herbs(self):
        result = (random.randint(1, self.basic_herb_gather)) * self.this_char['gather']
        return result

    def construct_hut(self):
        result = self.basic_fix_construct * self.this_char['fix_constr']
        if result > self.max_huts:
            result = self.max_huts
        return result

    def eat_herbs(self, herbs):
        amount_eaten = 2

        if herbs < 2:
            amount_eaten = herbs

        result = herbs - amount_eaten

        self.this_char['HP'] += self.this_char['health_reg']*amount_eaten
        if self.this_char['HP'] > 100:
            self.this_char['HP'] = 100

        return result

    def next_day_effect(self, temp, rain, wind, huts, food):
        temp_factor = 0
        food_factor = 0

        if math.fabs(temp-20) > 8:
            temp_factor = 2
        elif math.fabs(temp-20) > 15:
            temp_factor = 3

        if food < self.this_char['food_cons']:
            food_factor = self.this_char['food_cons'] - food

        self.this_char['HP'] -= ((temp_factor * self.this_char['cold_proof']) + rain + wind + food_factor - huts) * \
            self.this_char['health_los']


if __name__ == "__main__":
    # g = GameControl()
    c = Character('inf')
    print(c.this_char)
    print(c.ch_name)
    c.next_day_effect(30, 0, 0, 1, 5)
    print(c.this_char)
    print(c.bring_food())
    print(c.bring_herbs())
    print(c.construct_hut())
    print(c.eat_herbs(5))
    print(c.this_char)
