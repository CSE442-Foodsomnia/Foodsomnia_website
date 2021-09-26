from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, SubmitField, validators


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


    milk_allerg = BooleanField('Milk Allergy')
    peanut_allerg = BooleanField('Peanut Allergy')
    soybeans_allerg = BooleanField('Soybeans Allergy')
    wheat_allerg = BooleanField('Wheat Allergy')
    egg_allerg = BooleanField('Egg Allergy')
    fish_allerg = BooleanField('Fish Allergy')
    shellfish_alleg = BooleanField('Shellfish Allergy')


    accept_tos = BooleanField('I accept the Terms Of Service', [validators.DataRequired()])
    submit = SubmitField('Submit!')



class LoginForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password')
    submit = SubmitField('Submit!')
