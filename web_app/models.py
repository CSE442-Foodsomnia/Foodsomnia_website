from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = 'users'
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
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    spoonacular_id = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(), unique=True)
    image = db.Column(db.String(), unique=True)
    dairyFree = db.Column(db.Boolean(), default=False)
    glutenFree = db.Column(db.Boolean(), default=False)
    vegetarian = db.Column(db.Boolean(), default=False)
    ingredients = db.Column(db.String(), unique=False)
    summary = db.Column(db.String(), unique=True)
    author = db.Column(db.String(), unique=False)


    def __init__(self, spoonacular_id, title, image, dairyFree, glutenFree, vegetarian, ingredients, summary, author=""):
        self.spoonacular_id = spoonacular_id
        self.title = title
        self.image = image
        self.dairyFree = dairyFree
        self.glutenFree = glutenFree
        self.vegetarian = vegetarian
        self.ingredients = ingredients
        self.summary = summary
        self.author = author


    def __str__(self):
        return f"""spoonacular_id: {self.spoonacular_id},
                    title: {self.title},
                    image: {self.image},
                    dairyFree: {self.dairyFree},
                    glutenFree: {self.glutenFree},
                    vegetarian: {self.vegetarian},
                    ingredients: {self.ingredients},
                    summary: {self.summary},
                    author: {self.author}"""


class Ingredient():
     def __init__(self, name, amount, unit):
         self.name = name
         self.amount = amount
         self.unit = unit


class Liked(db.Model):
    __tablename__ = 'liked'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __init__(self, user_id, recipe_id, timestamp):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.pub_timestamp = timestamp


class Disliked(db.Model):
    __tablename__ = 'disliked'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __init__(self, user_id, recipe_id):
        self.user_id = user_id
        self.recipe_id = recipe_id
