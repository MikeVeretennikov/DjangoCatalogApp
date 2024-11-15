from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

import users.models

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Введите почту")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name")


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["coffee_count"].widget.attrs["readonly"] = True

    class Meta:
        model = users.models.Profile
        fields = ("birthday", "image", "coffee_count")


__all__ = []
