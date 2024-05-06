"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
dbx = db.session.execute


class Cupcake(db.Model):
    """Cupcake."""

    __tablename__ = "cupcakes"

    id = db.mapped_column(
        db.Integer,
        db.Identity(),
        primary_key=True,
    )

    flavor = db.mapped_column(
        db.String(50),
        nullable=False,
    )

    size = db.mapped_column(
        db.String(15),
        nullable=False,
    )

    rating = db.mapped_column(
        db.Integer(),
        nullable=False,
    )

    image_url = db.mapped_column(
        db.String(500),
        nullable=False,
        default="https://tinyurl.com/demo-cupcake"
    )

    # def serialize(self):
    #     """Serialize to dictionary."""

    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "calories": self.calories,
    #     }
