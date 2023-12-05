from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    # recipe.html & add-recipe.html
    path('recipe/<str:id>', views.recipe, name="recipe"),
    path('add-recipe/', views.add_recipe, name="add-recipe"),
    path('add_comment/<str:recipe>', views.add_comment, name="add_comment"),
    path('bookmark_toggle/', views.bookmark_toggle, name='bookmark_toggle'),

    # profile.html
    path('profile/<str:id>', views.profile, name="profile"),
    path('get_tab_data/', views.get_tab_data, name='get_tab_data'),
    path('delete_recipe/', views.delete_recipe, name='delete_recipe'),
    path('delete_comment/', views.delete_comment, name='delete_comment'),
    path('delete_bookmark/', views.delete_bookmark, name='delete_bookmark'),

]