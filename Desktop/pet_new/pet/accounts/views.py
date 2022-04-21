
from django.contrib.auth import views as views
from django.contrib.auth.views import PasswordChangeView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView

from pet.accounts.forms import CreateProfileForm, EditProfileForm, DeleteProfileForm
from pet.accounts.models import Profile
from pet.common.view_mixins import RedirectToDashboard
from pet.main.models import Pet, PetPhoto


class UserLoginView(views.LoginView):
    template_name = 'accounts/login_page.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()

class UserRegisterView(RedirectToDashboard, CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('dashboard')

class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pets = Pet.objects.filter(user_id=self.object.user_id)

        pet_photos = PetPhoto.objects \
            .filter(user_id=self.object.user_id) \
            .distinct()

        total_pet_photos_count = len(pet_photos)
        total_likes_count = 0
        for pt_photo in pet_photos:
            total_likes_count += len(pt_photo.like_set.all())

        context.update({
            'total_likes_count': total_likes_count,
            'pets': pets,
            'total_pet_photos_count': total_pet_photos_count,
            'is_owner': self.object.user_id == self.request.user.id
        })
        return context

class ChangeUserPasswordView(PasswordChangeView):
    template_name = 'accounts/change_password.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

class EditProfileView(UpdateView):
    form_class = EditProfileForm
    model = Profile
    template_name = 'accounts/profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('profile details',  kwargs={'pk': self.object.pk})

class DeleteProfileView(UpdateView):
    form_class = DeleteProfileForm
    model = Profile
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('index')
