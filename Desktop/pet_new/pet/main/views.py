from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views import generic as views

from pet.common.view_mixins import RedirectToDashboard
from pet.main.forms import CreatePetForm, EditPetForm, \
    DeletePetForm
from pet.main.models import PetPhoto, Pet, Like


class HomeView(RedirectToDashboard, views.TemplateView):
    template_name = 'main/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context



class DashboardView(views.ListView):
    model = PetPhoto
    template_name = 'main/dashboard.html'
    context_object_name = 'pet_photos'



class PetPhotoDetailsView(LoginRequiredMixin, views.DetailView):
    model = PetPhoto
    template_name = 'main/photo_details.html'
    context_object_name = 'pet_photo'

    def get_queryset(self):
        return super()\
            .get_queryset()\
            .prefetch_related('tagged_pets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet_photo = context['pet_photo']
        pet_photo_likes_list = Like.objects.filter(pet_photo=pet_photo)
        context['likes'] = len(pet_photo_likes_list)
        context['is_owner'] = self.object.user == self.request.user
        return context

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        viewed_pet_photos = request.session.get('last_viewed_pet_photo_ids', [])
        viewed_pet_photos.insert(0, self.kwargs['pk'])
        request.session['last_viewed_pet_photo_ids'] = viewed_pet_photos[:4]
        return response


def like_unlike_pet_photo(request, pk):
    pet_photo = PetPhoto.objects.get(pk=pk)
    the_user_like_list = Like.objects.filter(user = request.user.id, pet_photo=pet_photo)
    if len(the_user_like_list) > 0:
        the_user_like_list[0].delete()
    else:
        Like.objects.create(pet_photo=pet_photo, user=request.user)
    return redirect('pet photo details', pk)

class CreatePetView(views.CreateView):
    template_name = 'main/pet_create.html'
    form_class = CreatePetForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class EditPetView(views.UpdateView):
    template_name = 'main/pet_edit.html'
    form_class = EditPetForm

class DeletePetView(views.DeleteView):
    template_name = 'main/pet_delete.html'
    form_class = DeletePetForm


class CreatePetPhotoView(LoginRequiredMixin, views.CreateView):
    model = PetPhoto
    template_name = 'main/photo_create.html'
    fields = ('photo', 'description', 'tagged_pets')
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditPetPhotoView(views.UpdateView):
    model = PetPhoto
    template_name = 'main/photo_edit.html'
    fields = ['description', 'tagged_pets',]

    def get_success_url(self):
        return reverse_lazy('pet photo details', kwargs={'pk':self.object.id})

class DeletePetPhotoView(views.DeleteView):
    model = PetPhoto
    success_url = reverse_lazy('dashboard')