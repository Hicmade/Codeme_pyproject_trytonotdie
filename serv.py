from flask import Flask, render_template, request
from usables.game import GameControl, Character
from usables.dbhandler import GameDatabase


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_try():
    conditions = {}
    characters = {}

    if request.method == 'GET':
        conditions = GameControl().get_initial_conditions()
        characters = GameControl().get_new_characters()
        game_id = {'GameID': GameDatabase.input_gamedata(conditions)}
        GameDatabase.input_character_set(characters, game_id)

    #All below, not working yet...
    elif request.method == 'POST':
        GameID = request.form.get('GameID')
        db_game = GameDatabase.get_gamedata(GameID)
        db_ch = GameDatabase.get_character_set(GameID)
        #continue here...
        weather = GameControl.get_weather(data['temp'])
        day = {'day_number': data['day_number'] + 1}
        actions = []

        for key, value in data.items():
            if 'action' in key:
                if value == 'act1':
                    r = Character().bring_food()
                    data['food_supl'] += r

        print(actions)

    context = {}
    context.update(conditions)
    context.update(game_id)

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
