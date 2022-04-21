from django.urls import path

from pet.main.views import \
    like_unlike_pet_photo, \
    HomeView, DashboardView, CreatePetView, EditPetView, DeletePetView, CreatePetPhotoView, \
    PetPhotoDetailsView, EditPetPhotoView, DeletePetPhotoView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('photo/details/<int:pk>/', PetPhotoDetailsView.as_view(), name='pet photo details'),
    path('photo/add/', CreatePetPhotoView.as_view(), name='create pet photo'),
    path('photo/edit/<int:pk>', EditPetPhotoView.as_view(), name='edit pet photo'),
    path('photo/delete/<int:pk>', DeletePetPhotoView.as_view(), name='delete pet photo'),
    path('photo/like/<int:pk>/', like_unlike_pet_photo, name='like pet photo'),

    path('pet/add/', CreatePetView.as_view(), name='create pet'),
    path('pet/edit/<int:pk>/', EditPetView.as_view(), name='edit pet'),
    path('pet/delete/<int:pk>/', DeletePetView.as_view(), name='delete pet'),

]