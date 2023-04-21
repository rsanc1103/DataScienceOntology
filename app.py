from flask import *
from owlready2 import *


app = Flask(__name__)

@app.route('/')
def home():
    onto = get_ontology("/Users/robertosanchez/Desktop/gaming_popularity.owl").load()

    cl = list(onto.classes())

    games = onto.search(is_a = onto.Game)
    ranks = onto.search(is_a = onto.Rank)
    ratings = onto.search(is_a = onto.Rating)

    objectProperties = onto.object_properties()

    q = list(default_world.sparql("""
                            SELECT ?game
                            { ?game rdf:type owl:Class. }
            """))
    print(q)



    with onto:
        class Game(Thing):
            pass
        class Rating(Thing):
            pass
        class hasRating(ObjectProperty):
            domain = [Game]
            range = [str]

            for i in list(Rating.instances()):
                print(i.name)

            # Query
            # Game that hasRating value M
            results = list(onto.search(type=Game, hasRating=onto.E))
            for r in results:
                print(r.name)
                
            print(list(onto.object_properties()))

    return render_template("index.html", cl=cl, games=games, ranks=ranks, ratings=ratings, objectProperties=objectProperties)

@app.route('/save', methods=['POST'])
def save():
    onto = get_ontology("/Users/robertosanchez/Desktop/gaming_popularity.owl").load()
    gameName = request.form.get('game_name')
    new_game = onto.Game()
    new_game.name = gameName.replace(' ', '_')

    onto.save(file="/Users/robertosanchez/Desktop/gaming_popularity.owl", format="rdfxml")


    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
