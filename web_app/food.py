from flask import Blueprint, flash, render_template, redirect, url_for, session, request
from flask import jsonify
from random import randrange
import sys

from . import db
from .models import Recipe, Liked, Disliked
from flask_login import login_user, logout_user, login_required, current_user


food = Blueprint("food", __name__)

random_recipe_id = -1

@food.route("/food_rec", methods=['GET', 'POST'])
@login_required
def food_recommendation():
    """
    Function:
    Search through DB Liked table and recipe table then recommend a recipe that is similar
    """

    if request.method == 'POST':
        print("post!")
        key_pressed = request.get_json()["key_pressed"]
        print(f"keypressed: {key_pressed}")
        user_id = current_user.id

        print(user_id, recipe_id, file=sys.stdout)

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

    recipe_list = Recipe.query.all()

    i = randrange(0, len(recipe_list))
    random_recipe = recipe_list[i]
    global random_recipe_id
    random_recipe_id = random_recipe.id

    print(random_recipe_id)

    return render_template('swipe.html', recipe=random_recipe)


@food.route("/trending")
def trending():
    return render_template('home.html')


@food.route("/liked")
def liked():
    all_liked = Liked.query.filter_by(user_id=current_user.id)
    recipes = Recipe.query.filter(Recipe.id.in_([l.recipe_id for l in all_liked])).all()

    return render_template('liked.html', liked=recipes)


@food.route("/disliked")
def disliked():
    all_disliked = Disliked.query.filter_by(user_id=current_user.id)
    recipes = Recipe.query.filter(Recipe.id.in_([l.recipe_id for l in all_disliked])).all()

    return render_template('disliked.html', disliked=recipes)
