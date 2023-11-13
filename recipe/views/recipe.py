from django.shortcuts import render, get_object_or_404

import random

from ..utils import *

from ..models import Recipe

# Create your views here.
def home(request):
    recipes = Recipe.objects.all()
    
    # Shuffle the recipes and get a random subset
    recipes_list = list(recipes)
    random.shuffle(recipes_list)
    random_recipes = recipes_list[:6]

    for recipe in random_recipes:
        recipe.total_time = calculate_total_time(recipe)

    context = {'recipes': random_recipes}
    return render(request, 'home.html', context)

def recipe(request,id):
    recipe = get_object_or_404(Recipe, id=id)

    context = {'recipe':recipe}
    return render(request, 'recipe.html', context)
