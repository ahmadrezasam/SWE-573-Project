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
                    convert_to_fdc_unit(nutrient_unit)
                    nutrient_value = nutrient.get('value', 0)

                    amount_numeric = float(''.join(filter(str.isdigit, amount)))
                    
                    nutrient_key = f"{nutrient_name} ({nutrient_unit})"
                    serving_size = food_item.get('servingSize')
                    adjusted_value = nutrient_value
                    
                    if serving_size is not None and serving_size != 0:
                        adjusted_value = nutrient_value * (amount_numeric / serving_size)

                    if adjusted_value != 0:
                        if nutrient_key in nutrition_facts:
                            nutrition_facts[nutrient_key] += adjusted_value
                        else:
                            nutrition_facts[nutrient_key] = adjusted_value
    return nutrition_facts

def convert_to_fdc_unit(unit):
    unit_mapping = {
        "gr": "g",
        "kg": "kg",
        "mL": "ml",
        "l": "l",
        "c": "cup",
        "tbsp": "tablespoon",
        "tsp": "teaspoon",
        "oz": "ounce",
        "fl. oz": "fluid ounce",
        "lb": "pound",
    }

    fdc_unit = unit_mapping.get(unit)
    return fdc_unit

def calculate_bmi(weight_kg, height_m):
    if weight_kg is None or height_m is None:
        return None
    bmi = weight_kg / ((height_m/100) ** 2)
    return bmi