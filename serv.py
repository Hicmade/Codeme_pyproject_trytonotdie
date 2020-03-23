from flask import Flask, render_template
from game import game_control
from jinja2 import Environment, PackageLoader


app = Flask(__name__)

#@app.route('/')
def intro_page():
    env = Environment(loader=PackageLoader('__main__', '.'), trim_blocks=True)
    template = env.get_template('/templates/index.txt')
    output = template.render()
    print(output)
    return render_template('index.html')

@app.route('/')
def main_html():
    a = game_control()
    dic1 = a.character_names()
    dic2 = a.default_character_set()
    context = {**dic1, **dic2}
    return render_template('game.html', **context)


def start_game():
    a = game_control()
    print(a.default_character_set())
    print(a.character_names())
    pass


if __name__ == "__main__":
    app.run(debug=True)

