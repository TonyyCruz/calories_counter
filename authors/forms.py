import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(
        r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"
    )
    if not regex.match(password):
        raise ValidationError((
            "Password must have at least one uppercase letter, "
            "one lowercase letter and one special character. "
            "The length should be at least 8 characters."
        ),
            code="Invalid"
        )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "[a-z] [A-Z] [@*!#$%?...]",
        }),
        validators=[strong_password],
        help_text=(
            "Password must have at least 8 characters "
            "containing at least one uppercase, "
            "one lowercase and one special character."
        )
    )

    confirm_password = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Repeat you password",
        }),
        min_length=8,
    )

    username = forms.CharField(
        label='Username',
        required=True,
        help_text=(
            "Username must have letters, numbers or one of those @.+-_. "
            "The length should be between 4 and 150 characters."
        ),
        error_messages={
            "required": "This field must not be empty",
            "min_length": "Username must have at least 4 characters",
            "max_length": "Username must have less than 150 characters",
        },
        min_length=4,
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Ex.: @carol"
        }),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password"
        ]
        labels = {
            "first_name": "First name",
            "last_name": "Last name",
            "email": "E-mail",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "Ex.: Ana"
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Ex.: Carolina"
            }),
            "email": forms.TextInput(attrs={
                "placeholder": "Ex.: email@email.com"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            error_message = '"Password" and "Confirm password" must be equal'
            raise ValidationError({
                "confirm_password": error_message,
            },
                code="Invalid"
            )
