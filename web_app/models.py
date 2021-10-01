from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    milk_allerg = db.Column(db.Boolean)
    peanut_allerg = db.Column(db.Boolean)
    soybeans_allerg = db.Column(db.Boolean)
    wheat_allerg = db.Column(db.Boolean)
    egg_allerg = db.Column(db.Boolean)
    fish_allerg = db.Column(db.Boolean)
    shellfish_alleg = db.Column(db.Boolean)


    def __init__(self, email, username, password, milk_allerg, peanut_allerg,
    soybeans_allerg, wheat_allerg, egg_allerg, fish_allerg, shellfish_alleg):
        self.email = email
        self.username = username
        self.password = password
        self.milk_allerg = milk_allerg
        self.peanut_allerg = peanut_allerg
        self.soybeans_allerg = soybeans_allerg
        self.wheat_allerg = wheat_allerg
        self.egg_allerg = egg_allerg
        self.fish_allerg = fish_allerg
        self.shellfish_alleg = shellfish_alleg


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)
    image = db.Column(db.String(), unique=True)
