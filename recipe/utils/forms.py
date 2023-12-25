from django.forms import ModelForm
from django import forms
from requests import get

from recipe.models.user_profile import FoodAllergen
from ..models import Recipe, Category, UserProfile, User, DietGoal, UserComment

from django.contrib.auth.forms import  UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email address is already in use. Please use a different email.')
        return email

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ['ingredients', 'instructions', 'avg_rating', 'nutrition_facts', 'videos', 'images', 'creator']

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
        
    preparation_time = forms.CharField(widget=forms.TextInput(attrs={'type':'number', 'class': 'form-control d-inline', 'style':'width:6rem'}), required=False)
    cooking_time = forms.CharField(widget=forms.TextInput(attrs={'type':'number', 'class': 'form-control d-inline', 'style':'width:6rem'}), required=False)
# ------------------------------------------------------------

class UserForm(ModelForm):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        # fields = '__all__' 
        fields = ['description', 'height', 'weight', 'country', 'diet_goals', 'food_preference', 'food_allergens']


    food_preference = forms.ChoiceField(
        choices=UserProfile.FOOD_PREFERENCE_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    diet_goals = forms.ModelMultipleChoiceField(
        queryset=DietGoal.objects.all(),
        widget=forms.RadioSelect,
        required = False
    )

    food_allergens = forms.ModelMultipleChoiceField(
        queryset=FoodAllergen.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

#------------------------------------------------------------

class UserCommentForm(ModelForm):
    class Meta:
        model = UserComment
        fields = ['comment_text']

#------------------------------------------------------------