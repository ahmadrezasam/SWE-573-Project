from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

from .user_interaction import UserRating

import uuid

def image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'images/{filename}'

class Recipe(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.ManyToManyField('Category', null=True, blank=True) #Breakfast, lunch, dinner, ...
    description = models.TextField()
    ingredients = models.JSONField() # Dictionary { Ingredient : Amount}
    instructions = models.JSONField() # List [step1, step2, step3, ...]
    images = models.ImageField(null=True, blank=True, upload_to=image_file_path)
    videos = models.URLField(null=True, blank=True)
    nutrition_facts = models.JSONField(null=True, blank=True) #Dictionary {Nutrition(ex.protein) : Amount}
    preparation_time = models.PositiveIntegerField(null=True, blank=True)  # Time in minutes
    cooking_time = models.PositiveIntegerField(null=True, blank=True)  # Time in minutes
    created_at = models.DateTimeField(auto_now_add=True)
    avg_rating = models.FloatField(default=0)

    def calculate_avg_rating(self):
        ratings = UserRating.objects.filter(recipe=self)
        avg_rating = ratings.aggregate(Avg('value'))['value__avg']

        if avg_rating is not None:
            self.avg_rating = avg_rating
        else:
            self.avg_rating = 0

        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name