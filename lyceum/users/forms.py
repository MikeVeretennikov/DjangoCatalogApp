from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

import users.models

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Введите почту")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            User.username.field.name,
            User.email.field.name,
            "password1",
            "password2",
        )


class UserForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = User
        fields = (User.email.field.name, User.first_name.field.name)


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["coffee_count"].widget.attrs["disabled"] = True
        self.fields["image"].required = False
        self.fields["coffee_count"].required = False

    class Meta:
        model = users.models.Profile
        fields = (
            users.models.Profile.birthday.field.name,
            users.models.Profile.image.field.name,
            users.models.Profile.coffee_count.field.name,
        )

        widgets = {
            "birthday": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
        }


__all__ = ()
