from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('password/', views.password_change, name="password_change"),

    path('search/', views.search, name="search"),

    # recipe.html & add-recipe.html
    path('recipe/<str:id>', views.recipe, name="recipe"),
    path('add-recipe/', views.add_recipe, name="add_recipe"),
    path('edit-recipe/<int:recipe_id>', views.edit_recipe, name="edit_recipe"),
    path('add_comment/<str:recipe>', views.add_comment, name="add_comment"),
    path('bookmark_toggle/', views.bookmark_toggle, name='bookmark_toggle'),
    path('rating/', views.submit_rating, name='submit_rating'),

    # profile.html
    path('profile/', views.profile, name="profile"),
    path('get_tab_data/', views.get_tab_data, name='get_tab_data'),
    path('delete_recipe/', views.delete_recipe, name='delete_recipe'),
    path('delete_comment/', views.delete_comment, name='delete_comment'),
    path('delete_rating/', views.delete_rating, name='delete_rating'),
    # path('delete_bookmark/', views.delete_bookmark, name='delete_bookmark'),
]