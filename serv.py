from flask import Flask, render_template, request, redirect, url_for, get_flashed_messages, \
    make_response
from usables.game import GameControl, Character
from usables.dbhandler import GameDatabase


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def game():
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
        # gameid = {'GameID': data['GameID']} - obsolete, delete if working
        gameid = {'GameID' : request.cookies.get('cookie_game_id')}
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

    response = make_response(render_template('game.html', **context, ch=characters, GameID=gameid['GameID']))
    response.set_cookie('cookie_game_id', gameid)
    return response


@app.route("/save", methods=['get', 'post'])
def save():
    if request.method == 'GET':
        messages = get_flashed_messages()
        return render_template('save.html', messages=messages)

    if request.method == 'POST':
        gamename = request.form['save_name']
        password = request.form['save_pass']
        gameid = request.cookies.get('cookie_game_id')

        conditions = GameDatabase.get_gamedata(gameid)
        characters = GameDatabase.get_character_set(gameid)
        newgameid = {'GameID': GameDatabase.input_gamedata(conditions)}
        GameDatabase.input_character_set(characters, newgameid)

        credentials = {'user_id': gamename, 'user_pass': password, 'game_id' : newgameid}
        GameDatabase.save_game(credentials)

        response = make_response(redirect(url_for('game')))
        response.set_cookie('cookie_game_id', newgameid)

        return response

# from here!
@app.route("/load", methods=['get', 'post'])
def save():
    if request.method == 'GET':
        messages = get_flashed_messages()
        return render_template('load.html', messages=messages)

    if request.method == 'POST':
        gamename = request.form['save_name']
        password = request.form['save_pass']
        credentials = {'user_id' : gamename, 'user_pass' : password}
        gameid = request.cookies.get('cookie_game_id')

        conditions = GameDatabase.get_gamedata(gameid)
        conditions.update(credentials)
        characters = GameDatabase.get_character_set(gameid)
        newgameid = {'GameID': GameDatabase.input_gamedata(conditions)}
        GameDatabase.input_character_set(characters, newgameid)

        response = make_response(redirect(url_for('game')))
        response.set_cookie('cookie_game_id', newgameid)

        return response

if __name__ == "__main__":
    app.run(debug=True)
