import random
import math


class GameControl:


    @staticmethod
    def get_initial_conditions():
        init_conditions = {
            'temp': 20,
            'rain_txt': 'Clear sky',
            'wind_txt': 'No wind',
            'day': 1,
            'food_supl': 0,
            'herb_supl': 0,
            'huts': 0,
            'rain': 0,
            'wind': 0
        }

        return init_conditions

    @staticmethod
    def get_new_characters(number=4, randomly=False):
        occ_set = ['Doctor', 'Ranger', 'Engineer', 'Influencer']
        characters = []
        i = 0

        for x in range(number):
            if i > len(occ_set)-1:
                i = 0
            if randomly:
                ch = Character(random.choice(occ_set))

            else:
                ch = Character(occ_set[i])
                i += 1

            ch_dat = {"Ch_name": ch.ch_name, "Ch_occupation": ch.ch_occupation, "Ch_HP": ch.this_char['HP']}
            characters.append(ch_dat)

        return characters

    @staticmethod
    def get_weather(db_game):
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
        calculated_day = db_game['day'] + 1
        calculated_temp = random.randint(db_game['temp']-max_change, db_game['temp']+max_change)
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
            'wind_txt': calculated_wind['wind_txt'],
            'day': calculated_day
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
        choices = {'Doctor': self.t_doc, 'Ranger': self.t_ran, 'Engineer': self.t_eng, 'Influencer': self.t_inf}
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

    def construct_hut(self, now_huts):
        result = self.basic_fix_construct * self.this_char['fix_constr'] + now_huts
        if result > self.max_huts:
            result = self.max_huts
        return result

    def eat_herbs(self, herbs):
        amount_eaten = 2

        if herbs < 2:
            amount_eaten = herbs

        new_herbs = herbs - amount_eaten

        self.this_char['HP'] += round(self.this_char['health_reg']*amount_eaten)
        if self.this_char['HP'] > 100:
            self.this_char['HP'] = 100

        result = {
            'herbs': new_herbs,
            'HP': self.this_char['HP']
        }

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

        self.this_char['HP'] -= round(((temp_factor * self.this_char['cold_proof']) + rain + wind + food_factor - huts) * \
            self.this_char['health_los'])

        return self.this_char['HP']


if __name__ == "__main__":
    a = GameControl()

    print(a)
