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
        # Gets game conditions and characters referring to GameID
        data = request.form.to_dict()
        gameid = {'GameID': data['GameID']}
        db_game = GameDatabase.get_gamedata(gameid['GameID'])
        db_ch = GameDatabase.get_character_set(gameid['GameID'])

        next_day = GameControl.get_next_day(db_game, db_ch, data)
        db_game = next_day[0]
        db_ch = next_day[1]
        conditions = next_day[2]
        characters = next_day[3]

        GameDatabase.update_gamedata(db_game)
        GameDatabase.update_character_set(db_ch)

        conditions.update(db_game)

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
