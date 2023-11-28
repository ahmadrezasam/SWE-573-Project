from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, UpdateView
from ..models import User, UserProfile
from ..utils.forms import UserForm, UserProfileForm
from django.urls import reverse_lazy

class UserProfileDetailViewUpdateView(DetailView, UpdateView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'
    form_class = UserForm
    profile_form_class = UserProfileForm

    #The get_object method is overridden to return the current user.
    def get_object(self, queryset=None):
        return User.objects.order_by('?').first() # for testing purpose
        # return self.request.user # The current AUTHENTICATED user can be accessed via self.request.user.
    
    #The get_context_data method is overridden to include the user profile in the context.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create UserProfile instance for the current user
        user_profile = UserProfile.objects.get(user=self.object)
        context['user_profile'] = user_profile

        # Pass the UserProfile instance to the UserProfileForm as initial data
        context['profile_form'] = self.profile_form_class(instance=user_profile)
        
        return context

    #The get_success_url method is overridden to specify where the user should be redirected after a successful update.
    def get_success_url(self):
        return reverse_lazy('profile')
    
    def post(self, request):
        print(request.POST)
        self.object = self.get_object()
        user_form = self.form_class(request.POST, instance=self.object)
        user_profile = UserProfile.objects.get(user=self.object)
        profile_form = self.profile_form_class(request.POST, instance=user_profile)

        print(user_form)

        if user_form.is_valid() and profile_form.is_valid():
            print("VALIDDDDDDDDDDDD")
            user_form.save()
            profile_form.save()
            return self.form_valid(user_form)
        else:
            return self.form_invalid({'user_form': user_form, 'profile_form': profile_form})

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, forms):
        return render(self.request, self.template_name, context={'user_profile': forms['profile_form'].instance, 'user_form': forms['user_form'], 'profile_form': forms['profile_form']})

def profile(request):
    return UserProfileDetailViewUpdateView.as_view()(request)

# def profile(request):
#     user_profile = UserProfileForm()
#     user = UserForm()
    
#     if request.method == 'POST':
#         print(request.POST)
    
#     context = {'user_profile':user_profile,'user':user}
#     return render(request, 'profile.html', context)

# def update_profile(request, id):
#     user = get_object_or_404(User, id=id)
#     user_profile = get_object_or_404(UserProfile, user=user)
#     user_form = UserForm(request.POST or None, instance=user)
#     profile_form = UserProfileForm(request.POST or None, instance=user_profile)
#     if user_form.is_valid() and profile_form.is_valid():
#         user_form.save()
#         profile_form.save()
#         return redirect('profile')
#     context = {'form':user_form,'profile_form':profile_form}
#     return render(request, 'profile.html', context)