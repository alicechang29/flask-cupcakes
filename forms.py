"""Forms for cupcake app."""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional, AnyOf, URL, InputRequired, NumberRange


class AddCupcakeForm(FlaskForm):
    """Form for adding a pet."""

    flavor = StringField(
        "Cupcake Flavor",
        validators=[InputRequired()]
    )

    size = StringField(
        "Size",
        validators=[AnyOf(values=['small', 'medium', 'large'])]
    )

    rating = StringField(
        "Rating",
        validators=[NumberRange(min=0, max=10)]
    )

    image_url = StringField(
        "Image URL",
        validators=[
            URL(require_tld=False),  # should be true for prod
            Optional()
        ]
    )
