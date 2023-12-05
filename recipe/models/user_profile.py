from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)  # Height in centimeters
    weight = models.PositiveIntegerField(null=True, blank=True)  # Weight in kilograms
    country = CountryField(blank_label='(select country)', null=True, blank=True)
    diet_goals = models.ManyToManyField('DietGoal', null=True, blank=True) #lose weight, gain weight, ...
    food_allergens = models.ManyToManyField('FoodAllergen', null=True, blank=True) 

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    FOOD_PREFERENCE_CHOICES = [
        ('c', 'Omnivore'),
        ('vegan', 'Vegan'),
        ('vegetarian', 'Vegetarian'),
    ]
    food_preference = models.CharField(max_length=15, choices=FOOD_PREFERENCE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'UserProfile for {self.user.username}'
    
class FoodAllergen(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class DietGoal(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name   