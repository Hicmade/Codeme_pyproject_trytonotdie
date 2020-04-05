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
        conditions.update(gameid)
        GameDatabase.input_character_set(characters, gameid)

    elif request.method == 'POST':
        gameid_from_html = request.form.get('GameID')
        gameid = {'GameID': gameid_from_html}
        data = request.form.to_dict()
        db_game = GameDatabase.get_gamedata(gameid_from_html)
        db_ch = GameDatabase.get_character_set(gameid_from_html)
        weather = GameControl.get_weather(db_game['temp'])
        db_game.update(weather)
        day = {'day': db_game['day'] + 1}
        db_game.update(day)

        i = 0
        for key, value in data.items():
            if 'action' in key:
                if value == 'act1':
                    c = Character(db_ch[i]['Ch_occupation'])
                    r = c.bring_food()
                    db_game['food_supl'] += r
                elif value == 'act2':
                    r = Character(db_ch[i]['Ch_occupation']).bring_herbs()
                    db_game['herb_supl'] += r
                elif value == 'act3':
                    r = Character(db_ch[i]['Ch_occupation']).construct_hut(db_game['huts'])
                    db_game['huts'] = r
                elif value == 'act4':
                    r = Character(occup=db_ch[i]['Ch_occupation'], hp=db_ch[i]['Ch_HP']).eat_herbs(db_game['herbs'],
                                                                                                   db_ch[i]['HP'])
                    db_game['herb_supl'] = r['herbs']
                    db_ch[i]['HP'] = r['HP']
                i += 1

        GameDatabase.update_gamedata(db_game)
        GameDatabase.update_character_set(db_ch)
        conditions.update(db_game)
        conditions.update(gameid)
        characters = db_ch

    context = {}
    context.update(conditions)

    return render_template('game.html', **context, ch=characters)


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
