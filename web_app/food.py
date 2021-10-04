from flask import Blueprint, flash, render_template, redirect, url_for
from . import db
from .models import Recipe
from flask_login import login_user, logout_user, login_required, current_user


food = Blueprint("food", __name__)

@food.route("/food_rec", methods=['GET', 'POST'])
@login_required
def food_recommendation():
    """
    Function:
    Search through DB Liked table and recipe table then recommend a recipe that is similar
    """

    recipe = Recipe.query.all()[-1]

    return render_template('swipe.html', recipe=recipe)
