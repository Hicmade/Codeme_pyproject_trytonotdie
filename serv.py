from flask import Flask, render_template, request, redirect, url_for, get_flashed_messages, \
    make_response, flash
from usables.game import GameControl, Character
from usables.dbhandler import GameDatabase
import hashlib
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'slodki_blask_chmury_16_challenge'

@app.route('/', methods=['GET', 'POST'])
def game():
    conditions = {}
    characters = {}
    gameid = {'GameID': request.cookies.get('cookie_game_id')}

    if request.method == 'GET':
        if gameid['GameID'] is None or gameid['GameID'] == "0":
            conditions = GameControl().get_initial_conditions()
            characters = GameControl().get_new_characters()
            gameid['GameID'] = GameDatabase.input_gamedata(conditions)
            GameDatabase.input_character_set(characters, gameid)
        else:
            conditions = GameDatabase.get_gamedata(gameid['GameID'])
            characters = GameDatabase.get_character_set(gameid['GameID'])
            for x in characters:
                if x['Ch_HP'] <= 0:
                    x.update({'act_txt': 'I am dead!'})

    elif request.method == 'POST':
        # Gets game conditions and characters referring to GameID
        data = request.form.to_dict()

        gameid = {'GameID': int(request.cookies.get('cookie_game_id'))}
        db_game = GameDatabase.get_gamedata(gameid['GameID'])
        db_ch = GameDatabase.get_character_set(gameid['GameID'])

        next_day = GameControl.get_next_day(db_game, db_ch, data)
        db_game = next_day[0]
        db_ch = next_day[1]
        conditions = next_day[2]
        characters = next_day[3]

        # GameDatabase.update_gamedata(db_game)
        # GameDatabase.update_character_set(db_ch)
        gameid = {'GameID': GameDatabase.input_gamedata(db_game)}
        GameDatabase.input_character_set(db_ch, gameid)

        conditions.update(db_game)

    context = {}
    context.update(conditions)

    # print(GameControl.check_game(characters, db_game['day']))

    cookie_value = str(gameid['GameID'])
    response = make_response(render_template('game.html', **context, ch=characters, GameID=gameid['GameID']))
    response.set_cookie(key='cookie_game_id',
                        value=cookie_value)
    return response


@app.route("/save", methods=['get', 'post'])
def save():
    if request.method == 'GET':
        messages = get_flashed_messages()
        return render_template('save.html', messages=messages)

    if request.method == 'POST':
        gamename = request.form['save_name']
        password = request.form['save_pass']
        # salt = "34litery"
        # salted_pass = password + salt
        # hashed_pass = hashlib.md5(salted_pass.encode())
        gameid = int(request.cookies.get('cookie_game_id'))

        conditions = GameDatabase.get_gamedata(gameid)
        characters = GameDatabase.get_character_set(gameid)
        newgameid = {'GameID': GameDatabase.input_gamedata(conditions)}
        GameDatabase.input_character_set(characters, newgameid)

        credentials = {'user_id': gamename, 'user_pass': password, 'game_id': gameid}
        GameDatabase.save_game(credentials)

        response = make_response(redirect(url_for('game')))
        cookie_value = str(newgameid['GameID'])
        response.set_cookie(key='cookie_game_id',
                            value=cookie_value)

        return response


@app.route("/load", methods=['get', 'post'])
def load():
    if request.method == 'GET':
        messages = get_flashed_messages()
        return render_template('load.html', messages=messages)

    if request.method == 'POST':
        gamename = request.form['save_name']
        password = request.form['save_pass']
        credentials = {'user_id': gamename, 'user_pass': password}

        # data_from_db = GameDatabase.load_game(credentials)
        newgameid = GameDatabase.load_game(credentials)
        # hashed_password = data_from_db['User_pass']

        if newgameid == "0":

            flash('Wrong game name or password... keep trying :)')
            return redirect(url_for('load'))

        response = make_response(redirect(url_for('game')))
        cookie_value = str(newgameid)
        response.set_cookie(key='cookie_game_id',
                            value=cookie_value)

        return response


@app.route("/reset", methods=['get'])
def reset():
    response = make_response(redirect('/'))
    response.delete_cookie('cookie_game_id')

    return response


if __name__ == "__main__":
    app.run(debug=True)
