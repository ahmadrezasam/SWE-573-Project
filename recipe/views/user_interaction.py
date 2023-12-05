from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from ..utils.forms import UserCommentForm
from ..models import Recipe, UserComment, User, UserBookmark

def bookmark_toggle(request):
    try:
        user_id = 1
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
    
def delete_bookmark(request):
    try:
        bookmark_id = request.GET.get('id')
        bookmark = get_object_or_404(UserBookmark, pk=bookmark_id)
        bookmark.delete()
        return JsonResponse({"success": True, "message": "Bookmark deleted successfully"})
    except Exception as e:
        print(f"Error deleting bookmark: {e}")
        return JsonResponse({"success": False, "error": str(e)})
    
def add_comment(request, recipe_id):
    user_id = 1
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

def delete_comment(request):
    try:
        comment_id = request.GET.get('id')
        comment = get_object_or_404(UserComment, pk=comment_id)
        comment.delete()

        return JsonResponse({"success": True, "message": "Comment deleted successfully"})
    except Exception as e:
        # Log the error or handle it appropriately
        print(f"Error deleting comment: {e}")

        return JsonResponse({"success": False, "error": str(e)})