from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm, PasswordChangeForm, \
    UserCreationForm
from django import forms

from .models import User


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Адрес электронной почты'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
        }
    ))


class UserPasswordResetForm(PasswordResetForm):
    """
    A form that lets a user change set their password without entering the old
    password
    """

    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm).__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': 'Email',
               }))


class UserPasswordChangeForm(PasswordChangeForm):
    """
    A form that lets a user change set their password without entering the old
    password
    """

    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm).__init__(*args, **kwargs)

    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': 'Новый пароль',
               }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': 'Повторите пароль',
               }))


class RegisterUserForm(UserCreationForm):
    nickname = forms.CharField(label='', required=True,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Никнейм'}))
    email = forms.EmailField(label='', required=True,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(label='', required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='', required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ['nickname', 'email', 'password1', 'password2']