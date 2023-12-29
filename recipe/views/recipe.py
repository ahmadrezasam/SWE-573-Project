from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random, json

from django.conf import settings

from ..utils.utils import calculate_total_time, calculate_nutrition
from ..utils.forms import RecipeForm, UserCommentForm
from ..models import Recipe, UserComment, UserBookmark
from . import user_interaction

# from ..api.food_data_central import get_fdc_data

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

def search(request):
    query = request.GET.get('q', '')

    # Split the input query into a list of ingredients
    ingredients_list = [ingredient.strip() for ingredient in query.split(',')]
    # Create a Q object to combine queries for title and ingredients
    title_query = Q(title__icontains=query)
    ingredients_query = Q(ingredients__has_key=ingredients_list[0])

    for ingredient in ingredients_list:
            # Create a condition for each ingredient using the JSONField syntax
            condition = Q(ingredients__has_key=ingredient)
            ingredients_query &= condition

    # Combine the title and ingredients queries
    recipes = Recipe.objects.filter(title_query | ingredients_query)
    context = {'recipes': recipes, 'query': query}
    return render(request, 'components/home/search_result.html', context)

def home(request):
    random_recipes = get_random_recipes()
    for recipe in random_recipes:
        preparation_time_recipe_data(recipe)

    context = {'recipes': random_recipes}
    return render(request, 'home.html', context)

def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    allergy_foods = set()
    # Check if the user is authenticated
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        allergic_ingredients = set(user_profile.food_allergens.values_list('name', flat=True))
        recipe_ingredients = set(recipe.ingredients.keys())
        
        allergy_foods = allergic_ingredients.intersection(recipe_ingredients)
        
        # Use boolean values directly
        allergy_alert = bool(allergy_foods)
    else:
        allergy_alert = False

    comments = get_comments_for_recipe(recipe)
    comment_form = UserCommentForm()

    comments = get_comments_for_recipe(recipe)
    comment_form = UserCommentForm()
    is_bookmarked = UserBookmark.objects.filter(user=request.user.id, recipe=recipe).exists()

    if request.method == 'POST':
        handle_comment_post(request, id)

    context = {
        'recipe': recipe,
        'comments': comments,
        'comment_form': comment_form,
        'allergy_alert': allergy_alert,
        'allergy_foods': allergy_foods,
        'is_bookmarked': is_bookmarked,
    }
    
    return render(request, 'recipe.html', context)

@login_required(login_url='login')
def add_recipe(request):
    recipe_form = RecipeForm(request.POST, request.FILES)

    amounts = request.POST.getlist('amounts')  
    amount_units = request.POST.getlist('amountUnits')  
    ingredients = request.POST.getlist('ingredients')  
    instructions = request.POST.getlist('instructions')  

    instructions_data = json.dumps(instructions)
    instructions_data = json.loads(instructions_data)

    full_ingredients_data = {ingredient: f"{amount} {unit}" for ingredient, amount, unit in zip(ingredients, amounts, amount_units)}

    if request.method == 'POST' and recipe_form.is_valid():
        with transaction.atomic():
            new_recipe = recipe_form.save(commit=False) 
            new_recipe.instructions = instructions_data
            new_recipe.ingredients = full_ingredients_data
            new_recipe.creator = request.user
            # if new_recipe.ingredients != full_ingredients_data:
            new_recipe.nutrition_facts = calculate_nutrition(new_recipe.ingredients)
            new_recipe.save()
            recipe_form.save_m2m()  # Save many-to-many relationships if any
            return redirect('home')
    else:
        print(recipe_form.errors)

    context = {'recipe': recipe_form}
    return render(request, 'add-recipe.html', context)

@login_required(login_url='login')
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user != recipe.creator:
        return redirect('profile')
    
    edit_mode = True
    recipe_form = RecipeForm(instance=recipe)
    existing_instructions = recipe.instructions
    existing_ingredients = recipe.ingredients

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if recipe_form.is_valid():
            with transaction.atomic():
                new_recipe = recipe_form.save(commit=False) 

                amounts = request.POST.getlist('amounts')  
                amount_units = request.POST.getlist('amountUnits')  
                ingredients = request.POST.getlist('ingredients')  
                instructions = request.POST.getlist('instructions')  

                instructions_data = json.dumps(instructions)
                instructions_data = json.loads(instructions_data)

                full_ingredients_data = {ingredient: f"{amount} {unit}" for ingredient, amount, unit in zip(ingredients, amounts, amount_units)}

                new_recipe.instructions = instructions_data
                new_recipe.ingredients = full_ingredients_data

                if new_recipe.ingredients != existing_ingredients and new_recipe.ingredients != {} and existing_ingredients != {}:
                    new_recipe.nutrition_facts = calculate_nutrition(new_recipe.ingredients)

                new_recipe.save()
                recipe_form.save_m2m()  # Save many-to-many relationships if any
                return redirect('home')        
        else:
            print(recipe_form.errors)

    context = {'recipe': recipe, 'recipe_form': recipe_form, 'existing_steps': existing_instructions, 'existing_ingredients': existing_ingredients, 'edit_mode': edit_mode}
    return render(request, 'edit-recipe.html', context)

@login_required(login_url='login')
def delete_recipe(request):
    try:
        recipe_id = request.GET.get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.delete()
        return JsonResponse({"success": True, "message": "Recipe deleted successfully"})
    except Exception as e:
        print(f"Error deleting Recipe: {e}")
        return JsonResponse({"success": False, "error": str(e)})