from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.http import JsonResponse
import random, json

from django.conf import settings

from ..utils.utils import calculate_total_time
from ..utils.forms import RecipeForm, UserCommentForm
from ..models import Recipe, UserComment, UserBookmark
from . import user_interaction

from ..api.food_data_central import get_fdc_data

def get_random_recipes():
    recipes = Recipe.objects.all()
    recipes_list = list(recipes)
    random.shuffle(recipes_list)
    return recipes_list[:6]

def preparation_time_recipe_data(recipe):
    recipe.total_time = calculate_total_time(recipe)

def get_comments_for_recipe(recipe):
    return UserComment.objects.filter(recipe=recipe)

def handle_comment_post(request, recipe_id):
    user_interaction.add_comment(request, recipe_id)

def process_recipe_form(request):
    recipe = RecipeForm(request.POST)

    amounts = request.POST.getlist('amounts')  
    amount_units = request.POST.getlist('amountUnits')  
    ingredients = request.POST.getlist('ingredients')  
    instructions = request.POST.getlist('instructions')  

    instructions_data = json.dumps(instructions)
    instructions_data = json.loads(instructions_data)

    full_ingredients_data = {ingredient: f"{amount} {unit}" for ingredient, amount, unit in zip(ingredients, amounts, amount_units)}

    return recipe, instructions_data, full_ingredients_data

def save_recipe_and_redirect(recipe, instructions_data, full_ingredients_data):
    with transaction.atomic():
        new_recipe = recipe.save(commit=False)
        new_recipe.instructions = instructions_data
        new_recipe.ingredients = full_ingredients_data
        new_recipe.save()
        recipe.save_m2m()  # Save many-to-many relationships if any
        return redirect('home')

def home(request):
    random_recipes = get_random_recipes()
    for recipe in random_recipes:
        preparation_time_recipe_data(recipe)
    
    # fdc_data = get_fdc_data()
    # print(fdc_data)

    context = {'recipes': random_recipes}
    return render(request, 'home.html', context)

def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    comments = get_comments_for_recipe(recipe)
    comment_form = UserCommentForm()

    is_bookmarked = UserBookmark.objects.filter(user=1, recipe=recipe).exists()
    if is_bookmarked:
        recipe.is_bookmarked = True
    else:
        recipe.is_bookmarked = False

    print(recipe.is_bookmarked)

    if request.method == 'POST':
        handle_comment_post(request, recipe.id)

    context = {'recipe': recipe, 'comments': comments, 'comment_form': comment_form}
    
    return render(request, 'recipe.html', context)

def add_recipe(request):
    recipe, instructions_data, full_ingredients_data = process_recipe_form(request)

    if request.method == 'POST' and recipe.is_valid():
        return save_recipe_and_redirect(recipe, instructions_data, full_ingredients_data)
    else:
        print(recipe.errors)

    context = {'recipe': recipe}
    return render(request, 'add-recipe.html', context)

def delete_recipe(request):
    try:
        recipe_id = request.GET.get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.delete()
        return JsonResponse({"success": True, "message": "Recipe deleted successfully"})
    except Exception as e:
        print(f"Error deleting Recipe: {e}")
        return JsonResponse({"success": False, "error": str(e)})
