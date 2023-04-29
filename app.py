from flask import *
from owlready2 import *
import sys


app = Flask(__name__)


result = []

@app.route('/')
def home():
    # Define the `onto` namespace
    onto = get_ontology("gaming_popularity.owl").load()
    cl = list(onto.classes())
    games = onto.search(is_a = onto.Game)
    ratings = onto.search(is_a = onto.Rating)
    genres = onto.search(is_a = onto.Genre)
    objectProperties = list(onto.object_properties())
    dataProperties = list(onto.data_properties())

    results = result

    return render_template("index.html", cl=cl, games=games,genres=genres, ratings=ratings, objectProperties=objectProperties, dataProperties=dataProperties, results=results)

@app.route('/clear', methods=['POST'])
def clear():
    global result
    result = []
    return redirect(url_for('home'))


@app.route('/query', methods=['POST'])
def query():

    query = """
            PREFIX onto:<http://www.semanticweb.org/robertosanchez/ontologies/2023/2/gaming_popularity#>
            """
    query += request.form.get('sparql')
    qres = list(default_world.sparql(query))

    global result
    result = qres

    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
