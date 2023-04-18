from flask import Flask, render_template
from owlready2 import *


app = Flask(__name__)

@app.route('/')
def hello():
    onto = get_ontology("/Users/robertosanchez/Desktop/gaming_popularity.owl").load()
    Game_class = onto.Game
    new_game = onto.Game()

    cl = list(onto.classes())

    games = onto.search(is_a = onto.Game)
    ranks = onto.search(is_a = onto.Rank)
    ratings = onto.search(is_a = onto.Rating)

    # return 'Hello world'
    return render_template("index.html", cl=cl, games=games, ranks=ranks, ratings=ratings)

if __name__ == '__main__':
    app.run(debug=True)
