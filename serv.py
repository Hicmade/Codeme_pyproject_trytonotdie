from flask import Flask, render_template, request
from usables.game import GameControl, Character


app = Flask(__name__)


# @app.route('/')
def main_html():
    day = {"day_number": 1}
    resources = {"food_supl": 0, "herb_supl": 0, "huts_number": 0}
    weather = GameControl().get_initial_weather()

    ch1 = Character('doc')
    ch2 = Character('ran')
    ch3 = Character('eng')
    ch4 = Character('inf')

    characters = {
        "ch1_n": ch1.ch_name,
        "ch1_o": ch1.ch_occupation,
        "ch1_hp": ch1.this_char['HP'],
        "ch2_n": ch2.ch_name,
        "ch2_o": ch2.ch_occupation,
        "ch2_hp": ch2.this_char['HP'],
        "ch3_n": ch3.ch_name,
        "ch3_o": ch3.ch_occupation,
        "ch3_hp": ch3.this_char['HP'],
        "ch4_n": ch4.ch_name,
        "ch4_o": ch4.ch_occupation,
        "ch4_hp": ch4.this_char['HP'],
    }

    context = {}
    context.update(day)
    context.update(resources)
    context.update(weather)
    context.update(characters)
    print(context)

    return render_template('game_old.html', **context)


@app.route('/', methods=['GET', 'POST'])
def main_try():
    conditions = {}
    characters = {}

    if request.method == 'GET':
        conditions = GameControl().get_initial_conditions()
        characters = GameControl().get_new_characters()
        ch_number = {"ch_number": len(characters)}

    elif request.method == 'POST':
        data = request.form
        weather = GameControl.get_weather(data['temp'])
        day = {'day_number': data['day_number'] + 1}

        """for x in data:
            if x.key == "action"""



    context = {}
    context.update(conditions)
    context.update(ch_number)

    return render_template('game.html', **context, ch=characters)


@app.route("/game", methods=['get', 'post'])
def game():
    raw_data = request.form
    data = raw_data.to_dict()
    print(data)
    for key, value in data.items:
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
