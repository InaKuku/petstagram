import random
from django.test import TestCase
from django.urls import reverse
from pet.accounts.models import PetstagramUser
from pet.main.models import Pet


class DashboardViewTest(TestCase):

    VALID_USER_DATA = {
        'password': 'PetsyPass',
        'username': str(random.randint(0, 120000)),
        'date_joined': '2022-03-31',
        'is_staff': 'False'}

    user = PetstagramUser(**VALID_USER_DATA)
    user.full_clean()
    user.save()

    VALID_PET_DATA = {
        'name': str(random.randint(0, 120000)),
        'type': 'cat',
        'user': user
    }
    pet = Pet(**VALID_PET_DATA)
    pet.full_clean()
    pet.save()

    def test_get__expect_correct_template(self):
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed((response, 'main/dashboard.html'))



