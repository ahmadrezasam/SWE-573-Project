import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ..utils.forms import UserCommentForm
from ..models import Recipe, UserComment, User, UserBookmark, UserRating

@login_required(login_url='login')
def bookmark_toggle(request):
    try:
        user_id = request.user.id
        user = get_object_or_404(User, pk=user_id)
        recipe_id = request.GET.get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user_bookmark = UserBookmark.objects.filter(user=user, recipe=recipe)

        if user_bookmark.exists():
            user_bookmark.delete()
            return JsonResponse({"success": True, "is_bookmarked": False, "message": "Bookmark deleted successfully"})
        else:
            UserBookmark.objects.create(user=user, recipe=recipe)
            return JsonResponse({"success": True, "is_bookmarked": True, "message": "Bookmark created successfully"})
    except Exception as e:
        print(f"Error toggling bookmark: {e}")
        return JsonResponse({"success": False, "error": str(e)})

@login_required(login_url='login')
def add_comment(request, recipe_id):
    user_id = request.user.id
    user_instance = User.objects.get(pk=user_id)
    recipe_instance = Recipe.objects.get(pk=recipe_id)

    if request.method == 'POST':
        comment_form = UserCommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = user_instance
            new_comment.recipe = recipe_instance
            new_comment.save()
            return redirect('recipe', id=recipe_id)
        else:
            print(comment_form.errors)


@login_required(login_url='login')
def edit_comment(request, recipe_id, comment_id):
    comment = get_object_or_404(UserComment, pk=comment_id)
    comment_form = UserCommentForm(request.POST or None, instance=comment)

    if request.method == 'POST':
        if comment_form.is_valid():
            comment_form.save()
            return redirect('recipe', id=recipe_id)
        else:
            print(comment_form.errors)

    context = {
        'comment_form': comment_form,
        'comment': comment,
    }

    return render(request, 'edit_comment.html', context)

@login_required(login_url='login')
def delete_comment(request):
    try:
        comment_id = request.GET.get('id')
        comment = get_object_or_404(UserComment, pk=comment_id)
        comment.delete()
        return JsonResponse({"success": True, "message": "Comment deleted successfully"})
    except Exception as e:
        print(f"Error deleting comment: {e}")
        return JsonResponse({"success": False, "error": str(e)})

@require_POST
def submit_rating(request):
    try:
        # Load JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))
        
        user_id = request.user.id
        user = get_object_or_404(User, pk=user_id)
        recipe_id = data.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        rating_value = data.get('rating_value')

        # Check if the user has already rated the recipe
        existing_rating = UserRating.objects.filter(user=user, recipe=recipe).first()

        if existing_rating:
            # Update the existing rating
            existing_rating.value = rating_value
            existing_rating.save()
        else:
            # Create a new rating
            UserRating.objects.create(user=user, recipe=recipe, value=rating_value)

        # Recalculate the average rating
        recipe.calculate_avg_rating()

        return JsonResponse({'avg_rating': recipe.avg_rating, 'success': True})
    except Exception as e:
        print(f"Error submitting rating: {e}")
        return JsonResponse({"success": False, "error": str(e)})
    
def delete_rating(request):
    try:
        rating_id = request.GET.get('id')
        rating = get_object_or_404(UserRating, pk=rating_id)
        recipe_id = request.GET.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        rating.delete()
        # Recalculate the average rating
        recipe.calculate_avg_rating()
        return JsonResponse({"success": True, "message": "Rating deleted successfully"})
    except Exception as e:
        print(f"Error deleting rating: {e}")
        return JsonResponse({"success": False, "error": str(e)})