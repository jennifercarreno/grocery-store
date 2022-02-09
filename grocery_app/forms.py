from turtle import title
from unicodedata import category, name
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL

from grocery_app.models import GroceryStore

def stores():
    return GroceryStore.query.all()

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    title = StringField('Title', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')
   
class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], choices=['Produce', 'Deli', 'Bakery', 'Pantry', 'Frozen', 'Other'])
    photo_url = StringField('Photo Url', validators=[DataRequired()])
    # store = QuerySelectField(query_factory=stores, allow_blank=True)
    store = QuerySelectField('Store', query_factory=lambda: GroceryStore.query)


    submit = SubmitField('Submit')
