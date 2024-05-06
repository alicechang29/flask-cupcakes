"""Flask app for Cupcakes"""

import os
from flask import Flask, request, jsonify, render_template
from models import db, dbx, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///cupcakes')
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)


@app.get('/')
def show_cupcake_form():
    """Display the form for adding a cupcake"""

    return render_template("index.html")


@app.get("/api/cupcakes")
def list_all_cupcakes():
    """Return JSON of all cupcakes
    {'cupcakes': [{id, flavor, size, rating, image_url}, ...]}

    Cupcakes are ordered by rating.
    """

    q = db.select(Cupcake).order_by(Cupcake.rating.desc())
    cupcakes = dbx(q).scalars().all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def list_single_cupcake(cupcake_id):
    """Return JSON of a single cupcake
    {'cupcake': {id, flavor, size, rating, image_url}}
    """

    cupcake = db.get_or_404(Cupcake, cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post("/api/cupcakes")
def create_cupcake():
    """Create cupcake from posted JSON data & return it.
    Takes in cupcake attributes (flavor, size, rating, image_url).

    Returns JSON {'cupcake': {id, flavor, size, rating, image_url}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image_url = request.json.get("image_url")
    # checks request.json for image_url.
    # if it's none, will set it to default URL on 56

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image_url=image_url
    )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    # Return w/status code 201 --- return tuple (json, status)
    return (jsonify(cupcake=serialized), 201)


@app.patch("/api/cupcakes/<int:cupcake_id>")
def update_cupcake(cupcake_id):
    """Update the cupcake with cupcake_id using the attributes passed in by
    the user. FIXME: clarify what the attributes are
    Returns JSON {'cupcake': {id, flavor, size, rating, image_url}}
    """

    cupcake = db.get_or_404(Cupcake, cupcake_id)

    # is the below ok to handle multiple attributes?
    cupcake_attributes = {"flavor", "size", "rating", "image_url"}

    for attribute in request.json:
        if attribute in cupcake_attributes:
            setattr(cupcake, attribute, request.json[attribute])
        # FIXME: have else throw an error

    # will get flavor if it exists but will override flavor it exists or not
    # cupcake.flavor = request.json.get('flavor')

    # this works:
    # cupcake.flavor = request.json.get('flavor', cupcake.flavor)

    # we are checking truthy/falsy of request.json.get('size') -
        # which will be None if falsy and if cupcake.size was 0, will never be able to set it back to 0
    # cupcake.flavor = request.json.get('size') or cupcake.size

    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 200)


@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_cupcake(cupcake_id):
    """Delete the cupcake with cupcake_id.
    FIXME: fix the return json
    Returns JSON {'cupcake': {id, flavor, size, rating, image_url}}
    """

    cupcake = db.get_or_404(Cupcake, cupcake_id)
    db.session.delete(cupcake)

    db.session.commit()

    return (jsonify(deleted=cupcake_id), 200)

# TODO: how does browser know to refresh the data from a GET request if updates have been made behind the scenes? (insomnia?)
