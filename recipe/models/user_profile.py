from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)  # Height in centimeters
    weight = models.PositiveIntegerField(null=True, blank=True)  # Weight in kilograms
    country = CountryField(blank_label='(select country)', null=True, blank=True)
    diet_goals = models.ManyToManyField('DietGoal', null=True, blank=True)
    food_allergens = models.ManyToManyField('FoodAllergen', null=True, blank=True)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

class FoodAllergen(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class DietGoal(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name   