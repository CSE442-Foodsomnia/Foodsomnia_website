import copy
import random

class Recommender:
    def __init__(self, recipes, liked_recipes, disliked_recipes):
        self.recipes = copy.deepcopy(recipes)
        self.liked_recipes = copy.deepcopy(liked_recipes)
        self.liked_recipes = copy.deepcopy(disliked_recipes)
        self.percentAI = 0

    def recommend_recipe_random(self):
        return self.recipes.pop(random.randrange(len(self.recipes)))

    def recommend_recipe_ai(self):
        print('Hello World')


#if __name__ == "__main__":
#    rec = Recommender()