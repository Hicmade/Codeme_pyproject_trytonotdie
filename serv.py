from flask import Flask, render_template, request
from usables.game import GameControl, Character
from usables.dbhandler import GameDatabase


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_try():
    conditions = {}
    characters = {}
    gameid = None

    if request.method == 'GET':
        conditions = GameControl().get_initial_conditions()
        characters = GameControl().get_new_characters()
        gameid = {'GameID': GameDatabase.input_gamedata(conditions)}
        GameDatabase.input_character_set(characters, gameid)

    elif request.method == 'POST':
        # Gets game conditions and characters refering to GameID
        data = request.form.to_dict()
        gameid = {'GameID': data['GameID']}
        db_game = GameDatabase.get_gamedata(gameid['GameID'])
        db_ch = GameDatabase.get_character_set(gameid['GameID'])

        # Calculates new day
        weather = GameControl.get_weather(db_game)
        conditions.update(weather)

        # Calculates supplies
        supplies = {
            'food_supl': db_game['food_supl'],
            'herb_supl': db_game['herb_supl'],
            'huts': db_game['huts']
        }
        i = 0
        for key, value in data.items():
            if 'action' in key:
                if value == 'act1':
                    c = Character(db_ch[i]['Ch_occupation'])
                    r = c.bring_food()
                    supplies['food_supl'] += r
                elif value == 'act2':
                    c = Character(db_ch[i]['Ch_occupation'])
                    r = c.bring_herbs()
                    supplies['herb_supl'] += r
                elif value == 'act3':
                    c = Character(db_ch[i]['Ch_occupation'])
                    r = c.construct_hut(supplies['huts'])
                    supplies['huts'] = r
                elif value == 'act4':
                    c = Character(occup=db_ch[i]['Ch_occupation'], hp=db_ch[i]['Ch_HP'])
                    r = c.eat_herbs(supplies['herb_supl'])
                    supplies['herb_supl'] = r['herbs']
                    db_ch[i]['Ch_HP'] = r['HP']
                i += 1

        # Characters next day effect
        i = 0
        for x in db_ch:
            c = Character(occup=x['Ch_occupation'], hp=x['Ch_HP'])
            r = c.next_day_effect(temp=weather['temp'], rain=weather['rain'], wind=weather['wind'],
                              huts=supplies['huts'], food=supplies['food_supl'])
            db_ch[i].update({'Ch_HP': r})
            i += 1


        db_game.update(weather)
        db_game.update(supplies)

        GameDatabase.update_gamedata(db_game)
        GameDatabase.update_character_set(db_ch)

        conditions.update(db_game)
        characters = db_ch

    context = {}
    context.update(conditions)

    return render_template('game.html', **context, ch=characters, GameID=gameid['GameID'])


@app.route("/game", methods=['get', 'post'])
def game():

    raw_data = request.form
    data = raw_data.to_dict()
    print(data)
    for key in data:
        if 'action' in key:
            print(key)

    try1 = request.form.get('action1')
    try2 = request.form.get('action2')
    try3 = request.form.get('action3')
    try4 = request.form.get('action4')
    items = [
        {"akcja1": try1, "status": "udalo sie"},
        {"akcja1": try2, "status": "udalo sie"},
        {"akcja1": try3, "status": "udalo sie"},
        {"akcja1": try4, "status": "udalo sie"}
    ]
    return render_template('game.html', temp=data)


if __name__ == "__main__":
    app.run(debug=True)
