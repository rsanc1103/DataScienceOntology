from flask import *
from owlready2 import *
import sys


app = Flask(__name__)

@app.route('/')
def home():
    # Define the `onto` namespace
    onto = get_ontology("gaming_popularity.owl").load()
    cl = list(onto.classes())
    games = onto.search(is_a = onto.Game)
    ranks = onto.search(is_a = onto.Rank)
    ratings = onto.search(is_a = onto.Rating)
    objectProperties = list(onto.object_properties())
    dataProperties = list(onto.data_properties())

    return render_template("index.html", cl=cl, games=games, ranks=ranks, ratings=ratings, objectProperties=objectProperties, dataProperties=dataProperties)


@app.route('/query', methods=['POST'])
def query():
    if request.form.get('q_class') == 'Game':
        query = """
                    PREFIX onto:<http://www.semanticweb.org/robertosanchez/ontologies/2023/2/gaming_popularity#>
                    SELECT ?class
                    WHERE {{
                        ?class rdf:type onto:{} .
                        ?class onto:{} onto:{} .
                    }}
        """.format(request.form.get('q_class'), request.form.get('objectProperty'), request.form.get('q_rating'))

        if request.form.get('q_class') == 'Game' and request.form.get('objectProperty') == 'isRanked' or request.form.get('objectProperty') == 'genre':
            query = """
                        PREFIX onto:<http://www.semanticweb.org/robertosanchez/ontologies/2023/2/gaming_popularity#>
                        SELECT ?class
                        WHERE {{
                            ?class rdf:type onto:{} .
                            ?class onto:{} "{}" .
                        }}
            """.format(request.form.get('q_class'), request.form.get('objectProperty'), request.form.get('q_rank'))
            print(query)
        qres = list(default_world.sparql(query))
    elif request.form.get('q_class') == 'Rating':
        query = """
                        PREFIX onto:<http://www.semanticweb.org/robertosanchez/ontologies/2023/2/gaming_popularity#>
                        SELECT ?class
                        WHERE {{
                            ?class rdf:type onto:{} .
                        }}
        """.format(request.form.get('q_class'))
        qres = list(default_world.sparql(query))
    elif request.form.get('q_class') == 'Game' and request.form.get('objectProperty') == 'isRanked':
        query = """
                        PREFIX onto:<http://www.semanticweb.org/robertosanchez/ontologies/2023/2/gaming_popularity#>
                        SELECT ?class
                        WHERE {{
                            ?class rdf:type onto:{} .
                            ?class onto:{} "{}"^^xsd:integer .
                        }}
        """.format(request.form.get('q_class'), request.form.get('objectProperty'), request.form.get('q_rank'))
        
        
    return (str)(qres)


if __name__ == '__main__':
    app.run(debug=True)
