from django import forms
from pet.common.view_mixins import BootstrapFormMixin
from pet.main.models import Pet

class CreatePetForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        pet = super().save(commit=False)
        pet.user = self.user
        if commit:
            pet.save()
        return pet

    class Meta:
        model = Pet
        fields = ('name', 'type', 'date_of_birth',)
        widgets={
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter pet name',
                }
            ),
            'type': forms.Select(
                choices=Pet.TYPES,
                attrs={
                    'class': 'form-control',
                }
            ),

            'date_of_birth': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'min': '1920-01-01',
                }
            ),
        }

class EditPetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ('name', 'type', 'date_of_birth',)
        widgets={
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'type': forms.Select(
                choices=Pet.TYPES,
                attrs={
                    'class': 'form-control',
                }
            ),

            'date_of_birth': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'min': '1920-01-01',
                }
            ),
        }

class DeletePetForm(forms.ModelForm):
    def save(self, commit = True):
        self.instance.delete()
        return self.instance

    class Meta:
        model=Pet
        fields = ('name', 'type', 'date_of_birth',)
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'disabled': 'disabled'
                }
            ),
            'type': forms.Select(
                choices=Pet.TYPES,
                attrs={
                    'class': 'form-control',
                    'disabled': 'disabled'
                }
            ),

            'date_of_birth': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'min': '1920-01-01',
                    'disabled': 'disabled'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(DeletePetForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
# class DisabledFieldsFormMixin:
#     disabled_field = '__all__'
#     fields = {}
#
#     def _init_disabled_fields(self):
#         for name, field in self.fields.items():
#             if self.disabled_field != '__all__' and name not in self.disabled_field:
#                 continue
#             if not hasattr(field.widget, 'attrs'):
#                 setattr(field.widget, 'attrs', {})
#             field.widget.attrs['readonly'] += 'readonly'

# class EditPetPhotoForm(forms.ModelForm):
#     class Meta:
#         model = PetPhoto
#         fields = ('description', 'tagged_pets',)
#         widgets = {
#             'photo': forms.ClearableFileInput(
#             )
#         }
