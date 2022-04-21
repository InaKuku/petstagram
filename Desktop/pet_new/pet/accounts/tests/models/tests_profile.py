import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError
from pet.accounts.models import Profile, PetstagramUser

UserModel = get_user_model()

class ProfileTests(TestCase):
    VALID_USER_DATA = {
        'password': 'PetsyPass',
        'username': 'kjkhkkjghjhgnb',
        'date_joined': '2022-03-31',
        'is_staff': 'False'}


    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'Testov',
        'picture': 'https://softuni.bg/content/images/svg-logos/software-university-mobile-logo.svg',
        'gender': 'male',
    }


    def __create_valid_user_and_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_DATA)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        return (user, profile)



    def test_profile_create__when_first_and_last_name_contains_only_letters__expect_sucess(self):
        user, profile = self.__create_valid_user_and_profile()
        self.assertIsNotNone(profile.pk)


    def test_profile_create_when_first_name_contains_a_digit__expect_to_fail(self):
        user, profile = self.__create_valid_user_and_profile()
        first_name = 'Test1'
        profile.first_name = first_name

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)

    def test_profile_create_when_first_name_contains_a_dollar_sign__expect_to_fail(self):
        user, profile = self.__create_valid_user_and_profile()
        first_name = 'Don$cho'
        profile.first_name = first_name

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)

    def test_profile_create_when_first_name_contains_a_space__expect_to_fail(self):
        user, profile = self.__create_valid_user_and_profile()
        first_name = 'Don ch o'
        profile.first_name = first_name

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)

    def test_profile_create_when_last_name_contains_a_digit__expect_to_fail(self):
        user, profile = self.__create_valid_user_and_profile()
        last_name = 'Doey1'
        profile.last_name = last_name

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)

    def test_profile_create_when_last_name_contains_a_space__expect_to_fail(self):
        user, profile = self.__create_valid_user_and_profile()
        last_name = 'Doe y'
        profile.last_name = last_name

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)



