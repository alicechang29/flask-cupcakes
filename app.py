"""Flask app for Cupcakes"""

import os
from flask import Flask, request, jsonify
from models import db, dbx, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///cupcakes')
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)


@app.get("/api/cupcakes")
def list_all_cupcakes():
    """Return JSON {'cupcakes': [{id, flavor, size, rating, image_url}, ...]}
    FIXME: mention that returning all cupcakes
    Cupcakes are ordered by rating.
    """

    q = db.select(Cupcake).order_by(Cupcake.rating.desc())
    cupcakes = dbx(q).scalars().all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def list_single_cupcake(cupcake_id):
    """Return JSON {'cupcake': {id, flavor, size, rating, image_url}}
    FIXME: mention that returning 1 cupcake
    """

    cupcake = db.get_or_404(Cupcake, cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post("/api/cupcakes")
def create_cupcake():
    """Create cupcake from posted JSON data & return it.
    FIXME: document what json needs to be received into the route (show and tell)
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
    the user.
    Returns JSON {'cupcake': {id, flavor, size, rating, image_url}}
    """

    cupcake = db.get_or_404(Cupcake, cupcake_id)

    # is the below ok to handle multiple attributes?
    cupcake_attributes = {"flavor", "size", "rating", "image_url"}

    for attribute in request.json:
        if attribute in cupcake_attributes:
            setattr(cupcake, attribute, request.json[attribute])

    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 200)

@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_cupcake(cupcake_id):
    """Delete the cupcake with cupcake_id.
    Returns JSON {'cupcake': {id, flavor, size, rating, image_url}}
    """

    cupcake = db.get_or_404(Cupcake, cupcake_id)
    db.session.delete(cupcake)

    db.session.commit()

    return (jsonify(deleted=cupcake_id), 200)
