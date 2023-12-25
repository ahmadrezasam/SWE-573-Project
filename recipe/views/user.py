from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from os.path import join

from ..models import User, UserProfile, Recipe, UserComment, UserBookmark, UserRating
from ..utils.forms import RegisterForm, UserForm, UserProfileForm

# Global variable
profile_templates_path = 'components/profile/'

def get_user_and_profile(request, id):
    user_id = request.GET.get('id', id)
    user = get_object_or_404(User, id=user_id)
    user_profile = UserProfile.objects.get(user=user)
    return user, user_profile

def get_user_recipes(user):
    return Recipe.objects.filter(creator_id=user)

def get_user_comments(user):
    return UserComment.objects.filter(user_id=user)

def get_user_bookmarks(user):
    return UserBookmark.objects.filter(user_id=user)

def get_user_ratings(user):
    return UserRating.objects.filter(user_id=user)

def handle_user_forms(request, user, user_profile):
    user_form = UserForm(request.POST or None, instance=user)
    user_profile_form = UserProfileForm(request.POST or None, instance=user_profile)

    if request.method == 'POST':
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()

    return user_form, user_profile_form

def get_tab_data(request):
    user_id = request.GET.get('id')
    tab_name = request.GET.get('tab', 'recipes')  # Default to 'recipes' if no tab is specified
    data = ''
    
    if tab_name == 'recipes':
        data = render(request, join(profile_templates_path, 'recipes_table.html'), {'recipes': get_user_recipes(user_id)}).content
    elif tab_name == 'comments':
        data = render(request, join(profile_templates_path, 'comments_table.html'), {'comments': get_user_comments(user_id)}).content
    elif tab_name == 'bookmarks':
        data = render(request, join(profile_templates_path, 'bookmarks_table.html'), {'bookmarks': get_user_bookmarks(user_id)}).content
    elif tab_name == 'ratings':
        data = render(request, join(profile_templates_path, 'ratings_table.html'), {'ratings': get_user_ratings(user_id)}).content
    
    return JsonResponse({'table_html': data.decode('utf-8')})  # type: ignore

# url: /profile/
@login_required(login_url='login')
def profile(request):
    user = request.user
    user, user_profile = get_user_and_profile(request, user.id)
    user_form, user_profile_form = handle_user_forms(request, user, user_profile)

    # selected_tab = request.GET.get('tab', 'recipes')

    context = {
        'user': user,
        'user_profile': user_profile,
        'user_form': user_form,
        'user_profile_form': user_profile_form,
    }

    return render(request, 'profile.html', context)

def password_change(request):
    password_form = PasswordChangeForm(request.user, request.POST)
    if request.method == 'POST':
        if password_form.is_valid():
            user = password_form.save()
            auth_login(request, user)
            return redirect('profile')
        
    context = {'password_form': password_form}
    return render(request, join(profile_templates_path, 'change-password.html'), context)
           
def register(request):
    register_form = RegisterForm()
    email_exists_warning = False  # Initialize the variable

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data.get('email')
            if User.objects.filter(email__iexact=email).exists():
                email_exists_warning = True
            else:
                user = register_form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                # Check if UserProfile exists, create it if not
                UserProfile.objects.get_or_create(user=user)

                return redirect('login')

    context = {'register_form': register_form, 'email_exists_warning': email_exists_warning}
    return render(request, 'signup.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        
    return render(request, 'signin.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')