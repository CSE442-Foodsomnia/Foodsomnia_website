import copy
import random
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

class Recommender:
    def __init__(self, recipes, liked_recipes):
        self.recipes = copy.deepcopy(recipes)
        self.liked_recipes = copy.deepcopy(liked_recipes)
        #self.liked_recipes = copy.deepcopy(disliked_recipes)
        self.percentAIClass = PercentageAI()
        self.cosine_sim_class = CosineSimilarity(recipes)



    def recommend_recipe_random(self):
        return self.recipes.pop(random.randrange(len(self.recipes)))['title']

    def recommend_recipe_ai(self):
        cutoff_idx = 200
        target_recipe_index = self.cosine_sim_class.indices[random.choice(self.liked_recipes)]
        similarity_scores = pd.DataFrame(self.cosine_sim_class[target_recipe_index], columns=["score"])
        recipe_indices = similarity_scores.sort_values("score", ascending=False)[0:cutoff_idx].index
        rec_df = self.recipes['title'].iloc[recipe_indices]
        for i in range(1,cutoff_idx):
            if rec_df[i] not in self.liked_recipes:
                self.liked_recipes.append(rec_df[i])
                self.percentAIClass.incrementNumLiked()
                return rec_df[i]
        return self.recommend_recipe_random()


    def recommend_recipe(self):
        if random.uniform(0,100) <= self.percentAIClass.getPercentAI():
            return self.recommend_recipe_ai()
        else:
            return self.recommend_recipe_random()

    def updatedLikedRecipes(self,title):
        self.liked_recipes.append(title)

    def logout(self):
        return self.liked_recipes

class CosineSimilarity:
    def __init__(self, recipes):
        self.cosine_sim = self.createCosineSim(recipes)
        self.indices = self.titleToIndices(recipes)

    def titleToIndices(self, recipes):
        indices = pd.Series(recipes.index, index=recipes['title'])
        return indices[~indices.index.duplicated(keep='last')]

    def createCosineSim(self, recipes):
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(recipes['description'])
        return cosine_similarity(tfidf_matrix, tfidf_matrix)


class PercentageAI:
    def __init__(self):
        self.percentAI = 0
        self.numLiked = 0

    def changePercent(self):
        if self.numLiked == 10:
            self.percentAI = 20
        elif self.numLiked == 25:
            self.percentAI = 40

    def incrementNumLiked(self):
        self.numLiked += 1
        self.changePercent()

    def getPercentAI(self):
        return self.percentAI