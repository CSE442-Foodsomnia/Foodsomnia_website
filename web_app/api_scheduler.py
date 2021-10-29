from . import db, API_KEY
from .models import Recipe, Ingredient
import requests
import json
import sys
import re


RECIPE_COUNT = 50


JOKE = 0
INGREDIENT = 1
RECIPE = 2

def api_call(endpoint):
    """ endpoint can either be joke, ingredient, or recipe """


    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"

    headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': API_KEY
    }

    random_joke = "food/jokes/random"
    find = "recipes/findByIngredients"
    randomFind = f"https://api.spoonacular.com/recipes/random?apiKey={API_KEY}"

    response = None

    if endpoint == JOKE:
        pass
        # response =  str(requests.request("GET", url + random_joke, headers=headers).json()['text'])

    elif endpoint == INGREDIENT:
        pass
        # querystring = ""
        # response = requests.request("GET", url + find, headers=headers, params=querystring).json()

    elif endpoint == RECIPE:
        # Generate and store random recipe
        querystring = {"number": str(RECIPE_COUNT)}
        response = requests.request("GET", randomFind, headers=headers, params=querystring).json()

    return response




def store_recipes(app):
    """ Call API and store in DB """

    html_cleaner = re.compile('<.*?>')

    with app.app_context():

        # list of RECIPE_COUNT recipes
        recipes = api_call(RECIPE)['recipes']

        for r in recipes:
            ingredient_list = []
            for i in r["extendedIngredients"]:
                ingredient = Ingredient(i['name'],
                                        i['measures']['us']['amount'],
                                        i['measures']['us']['unitLong'])
                ingredient_list.append(json.dumps(ingredient.__dict__))



            clean_summary = re.sub(html_cleaner, '', r['summary'])
            print(clean_summary)
            print('================================================')
            rec_db = Recipe(r['id'],
                            r['title'],
                            r['image'],
                            r['dairyFree'],
                            r['glutenFree'],
                            r['vegetarian'],
                            ','.join(ingredient_list),
                            clean_summary,
                            r['sourceUrl'],
                            '')

            print(rec_db, sys.stdout)
            db.session.add(rec_db)
            db.session.commit()
            print(f"Added {RECIPE_COUNT} recipes to the recipe database")
