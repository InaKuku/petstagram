from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from pet.accounts.models import Profile
from pet.common.view_mixins import BootstrapFormMixin
from django import forms

from pet.main.models import PetPhoto, Pet

UserModel = get_user_model()

class CreateProfileForm(BootstrapFormMixin, UserCreationForm):

    first_name = forms.CharField(
        max_length = Profile.FIRST_NAME_MAX_LENGTH,
    )

    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
    )

    picture = forms.URLField()

    date_of_birth = forms.DateField()

    description = forms.CharField(
        widget=forms.Textarea
    )

    email = forms.EmailField()

    gender = forms.ChoiceField(
        choices=Profile.GENDERS
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            picture=self.cleaned_data['picture'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            description=self.cleaned_data['description'],
            email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],
            user=user,
        )
        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'picture', 'description')
        widgets={
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter first name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter last name'
                }
            ),
            'picture': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter URL'
                }
            ),
        }

class EditProfileForm(forms.ModelForm):
    MIN_DATE_OF_BIRTH = date(1920, 1, 1)
    MAX_DATE_OF_BIRTH = date.today()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['gender']=Profile.DO_NOT_SHOW

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth < self.MIN_DATE_OF_BIRTH or self.MAX_DATE_OF_BIRTH < date_of_birth:
            raise ValidationError(f'Date of birth must be between {self.MIN_DATE_OF_BIRTH} and {self.MAX_DATE_OF_BIRTH}')
        return date_of_birth

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'picture', 'date_of_birth', 'email', 'gender', 'description')
        widgets={
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter last name',
                }
            ),
            'picture': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter URL',
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    # 'min': '1920-01-01',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email',
                }
            ),
            'gender': forms.Select(
                choices=Profile.GENDERS,
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter description',
                    'rows': 3,
                }
            ),

        }

class DeleteProfileForm(forms.ModelForm):
    def save(self, commit = True):
        user = UserModel.objects.get(pk=self.instance.user_id)
        PetPhoto.objects.filter(user=user).delete()
        Pet.objects.filter(user=user).delete()
        self.instance.delete()
        user.delete()
        return self.instance

    class Meta:
        model=Profile
        fields=()

