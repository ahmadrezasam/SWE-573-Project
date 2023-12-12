from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, DietGoal, FoodAllergen

class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.diet_goal1 = DietGoal.objects.create(name='Lose Weight')
        self.diet_goal2 = DietGoal.objects.create(name='Gain Weight')
        self.allergen1 = FoodAllergen.objects.create(name='Peanuts')
        self.allergen2 = FoodAllergen.objects.create(name='Lactose')

        self.profile_data = {
            'user': self.user,
            'description': 'Test description',
            'height': 175,
            'weight': 70,
            'country': 'US',
            'gender': 'M',
            'food_preference': 'vegan',
        }

    def test_user_profile_creation(self):
        profile = UserProfile.objects.create(**self.profile_data)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.description, 'Test description')
        self.assertEqual(profile.height, 175)
        self.assertEqual(profile.weight, 70)
        self.assertEqual(profile.country, 'US')
        self.assertEqual(profile.gender, 'M')
        self.assertEqual(profile.food_preference, 'Omnivore')
        self.assertEqual(list(profile.diet_goals.all()), [])  # No diet goals initially
        self.assertEqual(list(profile.food_allergens.all()), [])  # No food allergens initially

    def test_user_profile_with_diet_goals_and_allergens(self):
        profile = UserProfile.objects.create(**self.profile_data)
        profile.diet_goals.add(self.diet_goal1, self.diet_goal2)
        profile.food_allergens.add(self.allergen1, self.allergen2)

        self.assertEqual(list(profile.diet_goals.all()), [self.diet_goal1, self.diet_goal2])
        self.assertEqual(list(profile.food_allergens.all()), [self.allergen1, self.allergen2])

    def test_user_profile_str_method(self):
        profile = UserProfile.objects.create(**self.profile_data)
        self.assertEqual(str(profile), f'UserProfile for {self.user.username}')

