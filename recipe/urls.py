from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('recipe/<str:id>', views.recipe, name="recipe"),
]