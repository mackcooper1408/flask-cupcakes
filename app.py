"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

connect_db(app)

debug = DebugToolbarExtension(app)


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

    new_cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = new_cupcake.serialize()

    return jsonify(cupcake=serialized)
