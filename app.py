from flask import *
from owlready2 import *
import sys


app = Flask(__name__)

@app.route('/')
def home():
    # Define the `onto` namespace
    onto = get_ontology("gaming_popularity.owl").load()
    




    # Create a SPARQL query using the `sparql` method
    qres = list(default_world.sparql("""
                                        PREFIX onto:<http://www.semanticweb.org/robertosanchez/ontologies/2023/2/gaming_popularity#>
                                        SELECT ?game
                                        WHERE{
                                            ?game rdf:type onto:Rating.
                                        }
    """))
    qres2 = list(default_world.sparql("""
                                        PREFIX onto:<http://www.semanticweb.org/robertosanchez/ontologies/2023/2/gaming_popularity#>
                                        SELECT ?game
                                        WHERE{
                                            ?game onto:hasRating onto:E.
                                        }
    """))

    qres3 = list(default_world.sparql("""
                                        PREFIX onto:<http://www.semanticweb.org/robertosanchez/ontologies/2023/2/gaming_popularity#>
                                        SELECT ?game
                                        WHERE {
                                            ?game rdf:type onto:Game .
                                            ?game onto:hasRating onto:M .
                                            ?game onto:rank 5 .
                                        }
    """))



    # Print the results
    # return (str)(qres3)


    cl = list(onto.classes())
    games = onto.search(is_a = onto.Game)
    ranks = onto.search(is_a = onto.Rank)
    ratings = onto.search(is_a = onto.Rating)
    objectProperties = list(onto.object_properties())

    return (str)(games[1])
    return render_template("index.html", cl=cl, games=games, ranks=ranks, ratings=ratings, objectProperties=objectProperties)

@app.route('/save', methods=['POST'])
def save():
    onto = get_ontology("gaming_popularity.owl").load()

    with onto:
        class Game(Thing):
            pass
        class Rating(Thing):
            pass
        class hasRating(ObjectProperty):
            domain = [Game]
            range = [str]

            # print Ratings instances
            for i in list(Rating.instances()):
                print(i.name)

            # Query
            # Game that hasRating value M
            results = list(onto.search(type=Game, hasRating=onto.E))
            for r in results:
                print(r.name)

            # print objectProperties
            print(list(onto.object_properties()))

    gameName = request.form.get('game_name')
    new_game = onto.Game()
    new_game.name = gameName.replace(' ', '_')

    # onto.save(file="gaming_popularity.owl", format="rdfxml")

    print(new_game)
    return redirect(url_for('home'))


@app.route('/query', methods=['POST'])
def query():
    onto = get_ontology("gaming_popularity.owl").load()

    res = []

    with onto:
        class Game(Thing):
            pass
        class Rating(Thing):
            pass
        class hasRating(ObjectProperty):
            domain = [Game]
            range = [str]

            # # print Ratings instances
            ratings_dic = {}
            for i in list(Rating.instances()):
                ratings_dic[i.name] = i

            # Query
            results = list(onto.search(type=Game, hasRating=ratings_dic[request.form.get('q_rating')]))
            
            for r in results:
                print(r.name)
                res.append(r.name)

    return (str)(res) 


if __name__ == '__main__':
    app.run(debug=True)
