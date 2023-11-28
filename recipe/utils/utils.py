# recipe_utils.py
import random
from math import ceil

def shuffle_recipes(recipes):
    recipes_list = list(recipes)
    random.shuffle(recipes_list)
    return recipes_list[:6]

def calculate_total_time(recipe):
    # Round up to the nearest 5 minutes
    return 5 * (ceil(int(recipe.preparation_time + recipe.cooking_time) / 5))

def calculate_bmi(weight, height):
    return round(weight / (height * height), 1)