from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask import jsonify
from random import randrange

from . import db
from .models import Recipe, Liked, Disliked
from flask_login import login_user, logout_user, login_required, current_user


food = Blueprint("food", __name__)


@food.route("/food_rec", methods=['GET', 'POST'])
@login_required
def food_recommendation():
    """
    Function:
    Search through DB Liked table and recipe table then recommend a recipe that is similar
    """

    recipe_list = Recipe.query.all()

    i = randrange(0, len(recipe_list))
    random_recipe = recipe_list[i]

    if request.method == 'POST':

        key_pressed = request.get_json()["key_pressed"]
        user_id = current_user.id
        recipe_id = random_recipe.id

        if key_pressed == 'left':
            new_dislike = Disliked(user_id, recipe_id)
            db.session.add(new_dislike)
            db.session.commit()
            print("added to dislike!")


        elif key_pressed == 'right':
            new_like = Liked(user_id, recipe_id)
            db.session.add(new_like)
            db.session.commit()
            print("added to liked!")

        else:
            print("wrong key pressed")

    return render_template('swipe.html', recipe=random_recipe)
