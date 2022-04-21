from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from pet.accounts.models import Profile
from pet.main.models import Pet, PetPhoto

UserModel = get_user_model()

class ProfileDetailsViewTests(TestCase):

    VALID_USER_CREDENTIALS = {'username': 'testuser', 'password': '12345qwe'}
    VALID_PROFILE_DATA = {'first_name': 'Test', 'last_name': 'User', 'picture': 'http:somepic/url.png', 'date_of_birth': date(1998, 4, 12),}
    VALID_PET_DATA = {'name': 'The petnanme', 'type': Pet.CAT}
    VALID_PET_PHOTO = {'photo': 'some.png', 'publication_date': date.today()}

    def __create_valid_user_and_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        return (user, profile)

    def __create_valid_pet_and_pet_photo(self, user):
        pet = Pet.objects.create(**self.VALID_PET_DATA, user=user)
        pet_photo = PetPhoto.objects.create(**self.VALID_PET_PHOTO, user=user)
        pet_photo.tagged_pets.add(pet)
        pet_photo.save()
        return (pet, pet_photo)

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)



    def test_when_openning_non_existing_profile__expect_404(self):
        response = self.client.get(reverse('profile details', kwargs = {'pk':1}))
        self.assertEqual(404, response.status_code)

    def test_when_user_is_owner__expect_is_owner_to_be_true(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs = {'pk':profile.pk}))
        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_to_be_false(self):
        user, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '12345qwe'
        }
        user2 = UserModel.objects.create_user(**credentials)
        self.client.login(**credentials)
        response = self.client.get(reverse('profile details', kwargs = {'pk':profile.pk}))
        self.assertFalse(response.context['is_owner'])

    def test_when_no_photos_likes__expect_total_likes_to_be_zero(self):
        user, profile = self.__create_valid_user_and_profile()
        pet, pet_photo = self.__create_valid_pet_and_pet_photo(user)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertEqual(0, response.context['total_likes_count'])

    def test_when_1_photos_likes__expect_total_likes_to_be_1(self):
        user, profile = self.__create_valid_user_and_profile()
        pet, pet_photo = self.__create_valid_pet_and_pet_photo(user)
        pet_photo.likes = 3
        pet_photo.save()
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertEqual(3, response.context['total_likes_count'])

    def test_when_no_photos_0_photos_count(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertEqual(0, response.context['total_pet_photos_count'])

    def test_when_user_has_pets__expect_to_return_only_users_pets(self):
        user, profile = self.__create_valid_user_and_profile()
        pet, _ = self.__create_valid_pet_and_pet_photo(user)

        credentials = {
            'username': 'testuser2',
            'password': '12345qwe'
        }
        pet2_data = {'name': 'Petty', 'type': Pet.DOG}

        user2 = UserModel.objects.create_user(**credentials)
        pet2 = Pet.objects.create(**pet2_data, user = user2)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertEqual([pet], response.context['pets'])

    def test_when_user_has_no_pets__expect_pets_to_be_empty_list(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertEqual([], response.context['pets'])

    def test_when_user_has_no_pets_likes_and_photos__expect_pets_to_be_empty_list_counts_to_be_zero(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertEqual([], response.context['pets'])
        self.assertEqual(0, response.context['total_pet_photos_count'])
        self.assertEqual(0, response.context['total_likes_count'])












