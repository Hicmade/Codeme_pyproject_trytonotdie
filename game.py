import random

class game_control:
    howmany = 4
    character_occupation = ["doctor", "ranger", "engineer", "influencer"]
    character_set = {"ch1" : None,
                     "ch2" : None,
                     "ch3" : None,
                     "ch4" : None,}
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

class character:
    t_doc = {
        'health_reg': 1.5,
        'health_los': 0.5,
        'heal': 4,
        'food_cons': 1,
        'hunt_eff' : 1,
        'cold_proof' : 1,
        'fix_constr' :1,
        'gather' : 1,
        'HP' : 100
    }

    t_ran = {
        'health_reg': 1.5,
        'health_los': 0.5,
        'heal': 2,
        'food_cons': 1.5,
        'hunt_eff' : 4,
        'cold_proof' : 0.5,
        'fix_constr' :2,
        'gather' : 1,
        'HP' : 100
    }

    t_eng = {
        'health_reg': 1,
        'health_los': 1,
        'heal': 1,
        'food_cons': 1.2,
        'hunt_eff' : 2,
        'cold_proof' : 1,
        'fix_constr' :4,
        'gather' : 1,
        'HP' : 100
    }

    t_inf = {
        'health_reg': 1,
        'health_los': 1,
        'heal': 1,
        'food_cons': 1,
        'hunt_eff' : 1,
        'cold_proof' : 1,
        'fix_constr' :1,
        'gather' : 1,
        'HP' : 100
    }
    this_char = {}

    def __init__(self, occup):
        choices = {'doc' : self.t_doc, 'ran' : self.t_ran, 'eng' : self.t_eng, 'inf' : self.t_inf}
        self.this_char = choices.get(occup, "something went wrong")


if __name__=="__main__":
    #g = game_control()
    c = character('inf')
    print(c.this_char)
