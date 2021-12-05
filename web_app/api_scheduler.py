from . import db, API_KEY
from .models import Recipe, Ingredient
import requests
import json
import sys
import re

from .models import Liked, Disliked, User
RECIPE_COUNT = 50
from flask_login import login_user, logout_user, login_required, current_user

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
            rec_db = Recipe(r['title'],
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
import smtplib
def send_email(app):
  gmail_user = 'foodsomnia.cse.buffalo@gmail.com'
  gmail_password = 'iixMvZQgPSV3nwL'
  trending_recipes, emails = trending(app)
  sent_from = gmail_user
  to = emails # User
  body = [ "#" + str(i + 1)  + '|' +  rec.title for i,rec in enumerate (trending_recipes)]
  body = "\n".join(body)
  email_text = """\
  From: %s
  To: %s
  Subject: %s
  Here are the top trending weekly recipes!
   
  %s
  """ % (sent_from, ", ".join(to), 'Food Somnia Website Trending Food Recipes Right Now!', body)


  try:
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(sent_from, to, email_text)
    smtp_server.close()
    print ("Email sent successfully!")
  except Exception as ex:
    print ("Something went wrong….",ex)
  return 

import pandas as pd 
import datetime 
from flask_login import login_user, logout_user, login_required, current_user
def trending(app):
   
     with app.app_context():
        # list of RECIPE_COUNT recipes
        users = User.query.all()
        emails = [u.email for u in users]
        df = pd.read_sql(Liked.query.statement, Liked.query.session.bind)
        one_month_datetime = datetime.datetime.now() - datetime.timedelta(days=30)
        one_month_ago_df = df[df['pub_timestamp'] > one_month_datetime]
        top_10_recipes = one_month_ago_df['recipe_id'].value_counts()[:10].index.tolist()
        recipes = Recipe.query.filter(Recipe.id.in_(top_10_recipes)).all()
        return recipes, emails 