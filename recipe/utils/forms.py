from django.forms import ModelForm
from django import forms
from ..models import Recipe, Category, UserProfile, User, DietGoal

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ['ingredients', 'instructions']

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    
    preparation_time = forms.CharField(widget=forms.TextInput(attrs={'type':'number', 'class': 'form-control d-inline', 'style':'width:6rem'}), required=False)
    cooking_time = forms.CharField(widget=forms.TextInput(attrs={'type':'number', 'class': 'form-control d-inline', 'style':'width:6rem'}), required=False)
    
    creator = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="---------", required=True)


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
        fields = ['description', 'height', 'weight', 'country', 'diet_goals', 'food_preference']


    food_preference = forms.ChoiceField(
        choices=UserProfile.FOOD_PREFERENCE_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    diet_goals = forms.ModelMultipleChoiceField(
        queryset=DietGoal.objects.all(),
        widget=forms.RadioSelect(attrs={'class': ''}),
    )
