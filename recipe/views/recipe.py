from django.shortcuts import render, get_object_or_404, redirect
import random, json

from ..utils.utils import calculate_total_time
from ..utils.forms import RecipeForm
from ..models import Recipe
from django.db import transaction

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

def add_recipe(request):
    recipe = RecipeForm()

    if request.method == 'POST':
        recipe = RecipeForm(request.POST)

        amounts = request.POST.getlist('amounts')  
        amountUnits = request.POST.getlist('amountUnits')  
        ingredients = request.POST.getlist('ingredients')  
        instructions = request.POST.getlist('instructions')  

        instructions_data = json.dumps(instructions)
        instructions_data = json.loads(instructions_data)

        full_ingredients_data = {ingredient: f"{amount} {unit}" for ingredient, amount, unit in zip(ingredients, amounts, amountUnits)}

        if recipe.is_valid():
            with transaction.atomic():
                new_recipe = recipe.save(commit=False)
                new_recipe.instructions = instructions_data
                new_recipe.ingredients = full_ingredients_data
                new_recipe.save()
                recipe.save_m2m()  # Save many-to-many relationships if any

                print("Recipe saved successfully")
                return redirect('home')
        else:
            print(recipe.errors)

    context = {'recipe': recipe}
    return render(request, 'add-recipe.html', context)