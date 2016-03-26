from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, SelectField, validators
#from wtforms.ext.sqlalchemy.fields import QuerySelectField
#from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired#, Required 
from wtforms.widgets import Select, TextArea


#Define and validate form for Restaurants.
class RestaurantForm(Form):
    """Sets definitions and validators for Shelter forms"""
    name = StringField('name', 
        [validators.InputRequired(), 
        validators.Length(
            max=20, 
            message="Limit 20 characters, please try again.")])
    address = StringField('address', 
        [validators.InputRequired(), 
        validators.Length(
            max=30, 
            message="Limit 30 characters, please try again.")])
    city = StringField('city', 
        [validators.InputRequired(), 
        validators.Length(
            max=20, 
            message="Limit 20 characters, please try again.")])
    state = StringField('state', 
        [validators.InputRequired(), 
        validators.Length(
            max=13, 
            message="Limit 13 characters, please try again.")])
    zipCode = StringField('zipCode', 
        [validators.InputRequired(), 
        validators.Length(
            max=10, 
            message="xxxxx or xxxxx-xxxx")])
    website = StringField('website', 
        [validators.InputRequired(),
        validators.URL(
            message="Not a valid URL (should contain http://www...)")])
    image = StringField('image', 
        [validators.InputRequired()])


#Define and validate form for Menu Items.
class MenuItemForm(Form):
    """Sets definitions and validators for Puppy forms"""
    name = StringField('name', 
        [validators.InputRequired(), 
        validators.Length(
            max=20, 
            message="Limit 50 characters, please try again.")])
    course = SelectField('course', 
            choices=[('Entree', 'Entree'), 
                ('Dessert', 'Dessert'), 
                ('Appetizer', 'Appetizer'),
                ('Beverage', 'Beverage')],
            widget=Select())
    description = TextAreaField('Needs', 
        [validators.InputRequired(
            message=('Please enter a detailed description of your dish.'))],
            widget=TextArea())
    image = StringField('image', 
        [validators.InputRequired()])
    price = IntegerField('price', 
        [validators.InputRequired()])


#Define and validate form for Users.
class UserForm(Form):
    """Sets definitions and validators for Owner forms"""
    name = StringField('name', 
        [validators.InputRequired(), 
        validators.Length(
            max=20, 
            message="Limit 15 characters.")])
    email = StringField('Email',
        [validators.InputRequired(
            message=('Email is required')),
        validators.Email(
            message=('Please enter a valid email address'))])
    picture = StringField('picture', 
        [validators.InputRequired()])