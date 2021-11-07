from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
import sys
import requests
from json import dumps

from . import db
from .models import User


views = Blueprint("views", __name__)

# @views.route("/nextImage")
# def nextImage():
#     url = "https://api.spoonacular.com/recipes/random"
#     querystring = {"number":1, "apiKey":"cb8ec284b4be41c7854eb79acd310ab1"}
#     response = requests.request("GET", url, params=querystring)
#     return dumps({'value': response.json()["recipes"][0]["image"], 'image': response.json()["recipes"][0]["image"], 'summary': response.json()["recipes"][0]["summary"], 'ingredients': response.json()["recipes"][0]["extendedIngredients"]})
#     #return response.json()["recipes"][0]["image"]
#
# global displayedText;
# theIngredients = ""
# def create_image():
#     print("WTF")
#     url = "https://api.spoonacular.com/recipes/random"
#     querystring = {"number":1, "apiKey":"cb8ec284b4be41c7854eb79acd310ab1"}
#     response = requests.request("GET", url, params=querystring)
#     global displayedText;
#     summary = response.json()["recipes"][0]["summary"]
#     ingredients = response.json()["recipes"][0]["extendedIngredients"]
#     global theIngredients
#     for x in ingredients:
#         theIngredients = theIngredients+x["name"]+","
#     theIngredients = theIngredients[:-1]
#     displayedText = summary
#     return response.json()["recipes"][0]["image"]



@views.route("/")
#@login_required
def home():
    print("home!", file=sys.stdout)
    return render_template("home.html")

@views.route("/database")
def database_show():
    user_list = User.query.all()
    return render_template("database.html", user_list=user_list)


@views.route("/database-delete")
def database_delete():
    pass
