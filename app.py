"""Flask app for Cupcakes"""

from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from forms import AddCupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

connect_db(app)

debug = DebugToolbarExtension(app)


@app.route("/")
def home():
    """ Render dynamic html page"""

    form = AddCupcake()

    return render_template("index.html", form=form)


@app.route("/api/cupcakes", methods=["POST"])
def add_new_cupcake():
    """ show list of all cupcakes """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


@app.route("/api/cupcakes")
def list_cupcake():
    """ show all cupcakes in database"""

    cupcakes = Cupcake.query.all()

    serialized = [c.serialize() for c in cupcakes]

    return (jsonify(cupcakes=serialized), 200)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """ Return information on cupcake"""
    new_cupcake = Cupcake.query.get(cupcake_id)

    if not new_cupcake:
        return ({"failed": "cupcake cannot be found"}, 404)

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 200)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PUT"])
def update_cupcake(cupcake_id):
    """ Update a cupcake by ID"""

    data = request.json

    new_cupcake = Cupcake.query.get(cupcake_id)

    if not new_cupcake:
        return ({"failed": "cupcake cannot be found"}, 404)

    new_cupcake.flavor = data['flavor']
    new_cupcake.size = data['size']
    new_cupcake.rating = data['rating']
    new_cupcake.image = data['image']

    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 200)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """ Delete a cupcake by ID"""

    new_cupcake = Cupcake.query.get(cupcake_id)

    if not new_cupcake:
        return ({"failed": "cupcake cannot be found"}, 404)

    db.session.delete(new_cupcake)
    db.session.commit()

    msg = {"message": "Deleted"}

    return (msg, 200)


@app.route("/api/cupcakes/search")
def search_cupcake():
    """ Search for a cupcake """
    search = request.args["searchTerm"]

    cupcakes = Cupcake.query.filter(Cupcake.flavor.ilike(f"%{search}%")).all()

    serialized = [c.serialize() for c in cupcakes]

    return (jsonify(cupcakes=serialized), 200)
