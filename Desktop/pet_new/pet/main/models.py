import datetime
from django.contrib.auth import get_user_model
from django.db import models
from pet.common.validators import MaxFileSizeInMbValidator

UserModel = get_user_model()


class Pet(models.Model):
    CAT = 'cat'
    DOG = 'dog'
    BUNNY = 'Bunny'
    PARROT = 'Parrot'
    FISH = 'Fish'
    OTHER = 'Other'
    TYPES = [(x, x) for x in (CAT, DOG, BUNNY, PARROT, FISH, OTHER)]

    NAME_MAX_LENGTH = 30

    name = models.CharField(
        max_length=NAME_MAX_LENGTH
    )

    type = models.CharField(
        max_length=max(len(x) for (x, _) in TYPES),
        choices=TYPES,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    user=models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.name}'

    @property
    def age(self):
        return datetime.datetime.now().year - self.date_of_birth.year

    class Meta:
        unique_together=('user', 'name')



class PetPhoto(models.Model):

    photo = models.ImageField(
        validators=(
            MaxFileSizeInMbValidator(5),
        )
    )

    tagged_pets = models.ManyToManyField(
        Pet,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

class Like(models.Model):

    pet_photo = models.ForeignKey(PetPhoto, on_delete=models.CASCADE)

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )