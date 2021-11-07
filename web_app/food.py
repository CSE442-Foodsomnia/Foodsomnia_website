from flask import Blueprint, flash, render_template, redirect, url_for, session, request
from flask import jsonify
from random import randrange
import sys

from . import db
from .models import Recipe, Liked, Disliked
from flask_login import login_user, logout_user, login_required, current_user
from .forms import RecipeForm


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
        displayed_recipe_id = request.get_json()["displayedrecipe"]
        print(f"keypressed: {key_pressed}")
        print(f"displayedrecipe: {displayed_recipe_id}")
        user_id = current_user.id

        # print(user_id, recipe_id, file=sys.stdout)

        if key_pressed == 'left':
            new_dislike = Disliked(user_id, displayed_recipe_id)
            db.session.add(new_dislike)
            db.session.commit()
            print("added to dislike!")


        elif key_pressed == 'right':
            new_like = Liked(user_id, displayed_recipe_id)
            db.session.add(new_like)
            db.session.commit()
            print("added to liked!")

        else:
            print("wrong key pressed")

    recipe_list = Recipe.query.all()

    i = randrange(0, len(recipe_list))
    random_recipe = recipe_list[i]
    print(random_recipe.title)

    return render_template('swipe.html', recipe=random_recipe, displayed_id=random_recipe.id)


@food.route("/trending")
def trending():
    return render_template('home.html')


@food.route("/liked", methods=['GET', 'POST'])
def liked():
    all_liked = Liked.query.filter_by(user_id=current_user.id).all()

    liked_recipes = []
    for like in all_liked:
        liked_recipes.append(Recipe.query.filter_by(id=like.recipe_id).first())

    return render_template('liked.html', liked=liked_recipes)

@food.route("/disliked", methods=['GET', 'POST'])
def disliked():
    all_disliked = Disliked.query.filter_by(user_id=current_user.id)
    recipes = Recipe.query.filter(Recipe.id.in_([l.recipe_id for l in all_disliked])).all()
    disliked_recipes = []
    for dislike in all_disliked:
        disliked_recipes.append(Recipe.query.filter_by(id=dislike.recipe_id).first())

    return render_template('disliked.html', disliked=disliked_recipes)


@food.route("/post", methods=['GET', 'POST'])
def post_recipe():
    # Recipe(r['id'],
    #                 r['title'],
    #                 r['image'],
    #                 r['dairyFree'],
    #                 r['glutenFree'],
    #                 r['vegetarian'],
    #                 ','.join(ingredient_list),
    #                 clean_summary,
    #                 r['sourceUrl'],
    #                 '')


    form = RecipeForm()
    if form.validate_on_submit():
        r = Recipe(form.title.data,
                    None,
                    form.dairyFree.data,
                    form.glutenFree.data,
                    form.vegetarian.data,
                    form.ingredients.data,
                    form.summary.data,
                    form.source_url.data,
                    current_user.username)

        db.session.add(r)
        db.session.commit()
        flash("Added the recipe to the database!", "success")

    return render_template("post_recipe.html", form=form)
