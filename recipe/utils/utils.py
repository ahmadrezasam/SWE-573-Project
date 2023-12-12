# recipe_utils.py
import random
from math import ceil
from ..api.food_data_central import search_food

def shuffle_recipes(recipes):
    recipes_list = list(recipes)
    random.shuffle(recipes_list)
    return recipes_list[:6]

def calculate_total_time(recipe):
    # Round up to the nearest 5 minutes
    return 5 * (ceil(int(recipe.preparation_time + recipe.cooking_time) / 5))

def calculate_bmi(weight, height):
    return round(weight / (height * height), 1)

def calculate_nutrition(data):
    nutrition_facts = {}
    for ingredient, amount in data.items():
        food_data = search_food(ingredient)
        if food_data and 'foods' in food_data:
            foods = food_data['foods']
            for food_item in foods:
                food_nutrition = food_item.get('foodNutrients', [])
                for nutrient in food_nutrition:
                    nutrient_name = nutrient.get('nutrientName')
                    nutrient_unit = nutrient.get('unitName')
                    nutrient_value = nutrient.get('value', 0)

                    amount_numeric = float(''.join(filter(str.isdigit, amount)))
                    
                    nutrient_key = f"{nutrient_name} ({nutrient_unit})"
                    adjusted_value = nutrient_value * (amount_numeric / food_item.get('servingSize'))

                    if nutrient_key in nutrition_facts:
                        nutrition_facts[nutrient_key] += adjusted_value
                    else:
                        nutrition_facts[nutrient_key] = adjusted_value
    return nutrition_facts