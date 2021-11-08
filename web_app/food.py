from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask import jsonify
from random import randrange
import json
import copy

import sys
import pandas as pd
from . import db
from .models import Recipe, Liked, Disliked, User
from flask_login import login_user, logout_user, login_required, current_user

import datetime
from .forms import RecipeForm



food = Blueprint("food", __name__)

random_recipe_id = -1

def nonAllergyLoop(recipedict, allergic_array):
    for key in recipedict:
        print("DFDFDF")
        print(key)
        print(type(key))
        if(type(key) == list):
            return True
        print(key["name"])
        for i in allergic_array:
            if i in key["name"]:
                return True
    return False

# we be forgettin comments out here
@food.route("/food_rec", methods=['GET', 'POST'])
@login_required
def food_recommendation():
    """
    Function:
    Search through DB Liked table and recipe table then recommend a recipe that is similar
    """
    value = User.query.filter_by(id=current_user.id).all()

    allergic_array = []
    if((value[0]).egg_allerg == True):
        allergic_array.append("egg")
        allergic_array.append("white cake mix")
        allergic_array.append("meringue")
        allergic_array.append("mayonnaise")
    if((value[0]).fish_allerg == True):
        allergic_array.append("fish")
        allergic_array.append("anchovies")
        allergic_array.append("caviar")
        allergic_array.append("roe")
        allergic_array.append("sushi")
        allergic_array.append("shark")
        allergic_array.append("seafood")
    if((value[0]).milk_allerg == True):
        allergic_array.append("milk")
        allergic_array.append("butter")
        allergic_array.append("cheese")
        allergic_array.append("cream")
        allergic_array.append("ranch")
        allergic_array.append("yogurt")
        allergic_array.append("whey")
    if((value[0]).peanut_allerg == True):
        allergic_array.append("peanuts")
        allergic_array.append("peanut butter")
        allergic_array.append("mixed nuts")
        allergic_array.append("peanut oil")
    if ((value[0]).shellfish_alleg == True):
        allergic_array.append("shellfish")
        allergic_array.append("crab")
        allergic_array.append("krill")
        allergic_array.append("lobster")
        allergic_array.append("shrimp")
    if ((value[0]).soybeans_allerg == True):
        allergic_array.append("soy bean")
        allergic_array.append("soy")
        allergic_array.append("tofu")
        allergic_array.append("miso")
        allergic_array.append("edamame")

    if ((value[0]).wheat_allerg == True):
        allergic_array.append("wheat")
        allergic_array.append("bread")
        allergic_array.append("pasta")
        allergic_array.append("flour")
        allergic_array.append("cracker")
        allergic_array.append("crouton")

    print(allergic_array)
    recipe_list = Recipe.query.all()

    new_list = copy.deepcopy(recipe_list)
    i = randrange(0, len(new_list))
    random_recipe = new_list[i]

    random_recipe.ingredients ="["+random_recipe.ingredients + "]"
    print(random_recipe.ingredients)
    print("WWWWWWW")
    recipedict = json.loads(random_recipe.ingredients)
    redo = True
    while(redo == True):
        if(nonAllergyLoop(recipedict, allergic_array) == True):
            redo = True
            i = randrange(0, len(recipe_list))
            random_recipe = new_list[i]
            random_recipe.ingredients = "[" + random_recipe.ingredients + "]"
            recipedict = json.loads(random_recipe.ingredients)
        else:
            redo = False

    #print(random_recipe.ingredients)


    if request.method == 'POST':
        print("post!")
        key_pressed = request.get_json()["key_pressed"]
        displayed_recipe_id = request.get_json()["displayedrecipe"]
        print(f"keypressed: {key_pressed}")
        print(f"displayedrecipe: {displayed_recipe_id}")
        user_id = current_user.id
        recipe_id = request.get_json()["displayedrecipe"]

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

    random_recipe_ingredients = ""
    for key in recipedict:
        random_recipe_ingredients = random_recipe_ingredients + key["name"] + ", "
    random_recipe_ingredients = random_recipe_ingredients[:-2]
    # for i in random_recipe.ingredients:
    #     random_recipe_ingredients = random_recipe_ingredients + i[0]["name"]
    #print(random_recipe.ingredients[0])

    return render_template('swipe.html', recipe=random_recipe, displayed_id=random_recipe.id, ingredients = random_recipe_ingredients)



@food.route("/Trending")
def trending():
    df = pd.read_sql(Liked.query.statement, Liked.query.session.bind)

    one_month_datetime = datetime.datetime.now() - datetime.timedelta(days=30)
    one_month_ago_df = df[df['pub_timestamp'] > one_month_datetime]
    top_10_recipes = one_month_ago_df['recipe_id'].value_counts()[:10].index.tolist()
    recipes = Recipe.query.filter(Recipe.id.in_(top_10_recipes)).all()

    return render_template('trending.html', trending_recipes = recipes)


@food.route("/liked", methods=['GET', 'POST'])
def liked():
    all_liked = Liked.query.filter_by(user_id=current_user.id).all()

    liked_recipes = []
    for like in all_liked:
        liked_recipes.append(Recipe.query.filter_by(id=like.recipe_id).first())
    print(liked_recipes)
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


    return render_template('disliked.html', disliked=disliked_recipes)
@food.route("/profile")
def profile():
    value = User.query.filter_by(id=current_user.id).all()
    eggallerg = value[0].egg_allerg
    fishallerg = value[0].fish_allerg
    milkallerg = value[0].milk_allerg
    peanutallerg = value[0].peanut_allerg
    shellfishallerg=value[0].shellfish_alleg
    soybeanallerg=value[0].soybeans_allerg
    wheatallerg = value[0].wheat_allerg
    return render_template('profile.html',name=current_user.username, ea=eggallerg, fa=fishallerg, ma=milkallerg, pa=peanutallerg, sfa = shellfishallerg, sba = soybeanallerg, wa = wheatallerg)