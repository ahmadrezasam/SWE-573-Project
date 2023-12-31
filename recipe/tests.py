from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *

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
        self.assertEqual(profile.food_preference, 'vegan')
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

class RecipeModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a category for testing
        self.category = Category.objects.create(name='Test Category')

        # Create a recipe for testing
        self.recipe = Recipe.objects.create(
            creator=self.user,
            title='Test Recipe',
            description='Test description',
            ingredients={'Ingredient1': 'Amount1', 'Ingredient2': 'Amount2'},
            instructions=['Step 1', 'Step 2', 'Step 3'],
            preparation_time=30,
            cooking_time=45
        )

        # Add the category to the recipe using the add() method
        self.recipe.category.add(self.category)

        # Create user ratings for the recipe
        UserRating.objects.create(user=self.user, recipe=self.recipe, value=5)
        UserRating.objects.create(user=self.user, recipe=self.recipe, value=4)


    def test_calculate_avg_rating(self):
        # Calculate the average rating for the recipe
        self.recipe.calculate_avg_rating()

        # Retrieve the updated recipe from the database
        updated_recipe = Recipe.objects.get(pk=self.recipe.pk)

        # Check if the average rating is calculated correctly
        self.assertEqual(updated_recipe.avg_rating, 4.5)

    def test_category_str_method(self):
        # Check if the __str__ method of the Category model works correctly
        self.assertEqual(str(self.category), 'Test Category')

class UserInteractionModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a recipe for testing
        self.recipe = Recipe.objects.create(
            creator=self.user,
            title='Test Recipe',
            description='Test description',
            ingredients={'Ingredient1': 'Amount1', 'Ingredient2': 'Amount2'},
            instructions=['Step 1', 'Step 2', 'Step 3'],
            preparation_time=30,
            cooking_time=45
        )

    def test_user_bookmark(self):
        bookmark = UserBookmark.objects.create(user=self.user, recipe=self.recipe)
        self.assertTrue(UserBookmark.objects.filter(pk=bookmark.pk).exists())

    def test_user_like(self):
        like = UserLike.objects.create(user=self.user, recipe=self.recipe)
        self.assertTrue(UserLike.objects.filter(pk=like.pk).exists())

    def test_user_comment(self):
        comment = UserComment.objects.create(user=self.user, recipe=self.recipe, comment_text='Test comment')
        self.assertTrue(UserComment.objects.filter(pk=comment.pk).exists())

    def test_user_review(self):
        review = UserReview.objects.create(user=self.user, recipe=self.recipe, review_text='Test review')
        self.assertTrue(UserReview.objects.filter(pk=review.pk).exists())

    def test_user_rating(self):
        rating = UserRating.objects.create(user=self.user, recipe=self.recipe, value=4)
        self.assertTrue(UserRating.objects.filter(pk=rating.pk).exists())

class RecipeViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.recipe = Recipe.objects.create(
            creator=self.user,
            title='Test Recipe',
            description='Test description',
            ingredients={'Ingredient1': 'Amount1', 'Ingredient2': 'Amount2'},
            instructions=['Step 1', 'Step 2', 'Step 3'],
            preparation_time=30,
            cooking_time=45
        )
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_recipe_view(self):
        response = self.client.get(reverse('recipe', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe.html')

    def test_add_recipe_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add-recipe.html')

    def test_edit_recipe_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('edit_recipe', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit-recipe.html')

    def test_delete_recipe_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('delete_recipe'), {'id': self.recipe.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.assertEqual(Recipe.objects.count(), 0)

class ProfileViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.client = Client()

    def test_profile_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_password_change_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/profile/change-password.html')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')

    def test_logout_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects to home page after logout
        self.assertRedirects(response, reverse('home'))

class ProfileDataTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.recipe = Recipe.objects.create(
            creator=self.user,
            title='Test Recipe',
            description='Test description',
            ingredients={'Ingredient1': 'Amount1', 'Ingredient2': 'Amount2'},
            instructions=['Step 1', 'Step 2', 'Step 3'],
            preparation_time=30,
            cooking_time=45
        )
        self.comment = UserComment.objects.create(user=self.user, recipe=self.recipe, comment_text='Test comment')
        self.bookmark = UserBookmark.objects.create(user=self.user, recipe=self.recipe)
        self.rating = UserRating.objects.create(user=self.user, recipe=self.recipe, value=4)
        self.client = Client()

    def test_get_user_recipes(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('get_tab_data'), {'id': self.user.id, 'tab': 'recipes'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Recipe', response.json()['table_html'])

    def test_get_user_comments(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('get_tab_data'), {'id': self.user.id, 'tab': 'comments'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test comment', response.json()['table_html'])

    def test_get_user_bookmarks(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('get_tab_data'), {'id': self.user.id, 'tab': 'bookmarks'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Recipe', response.json()['table_html'])

    def test_get_user_ratings(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('get_tab_data'), {'id': self.user.id, 'tab': 'ratings'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Recipe', response.json()['table_html'])