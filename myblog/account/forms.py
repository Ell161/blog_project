from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm, PasswordChangeForm, \
    UserCreationForm
from django import forms
from .models import User


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'field-update-form', 'placeholder': 'Адрес электронной почты'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'field-update-form',
            'placeholder': 'Пароль',
        }
    ))


class UserPasswordResetForm(PasswordResetForm):
    """
    A form that lets a user change set their password without entering the old
    password
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.PasswordInput(
        attrs={'class': 'field-update-form',
               'placeholder': 'Email',
               'type': 'email'
               }))


class UserPasswordChangeForm(PasswordChangeForm):
    """
    A form that lets a user change set their password without entering the old
    password
    """

    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm).__init__(*args, **kwargs)

    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'field-update-form',
               'placeholder': 'Новый пароль',
               'autocomplete': 'off'
               }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'field-update-form',
               'placeholder': 'Повторите пароль',
               'autocomplete': 'off'
               }))


class RegisterUserForm(UserCreationForm):
    nickname = forms.CharField(label='', required=True,
                               widget=forms.TextInput(
                                   attrs={'class': 'field-update-form',
                                          'placeholder': 'Никнейм',
                                          'autocomplete': 'off'}))
    email = forms.EmailField(label='', required=True,
                             widget=forms.EmailInput(
                                 attrs={'class': 'field-update-form',
                                        'placeholder': 'Email',
                                        'autocomplete': 'off'}))
    password1 = forms.CharField(label='', required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'field-update-form',
                                           'placeholder': 'Введите пароль',
                                           'autocomplete': 'new-password'}))
    password2 = forms.CharField(label='', required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'field-update-form',
                                           'placeholder': 'Повторите пароль',
                                           'autocomplete': 'new-password'}))

    class Meta:
        model = User
        fields = ('nickname', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('avatar', 'nickname', 'last_name', 'first_name', 'birthday', 'email',)
        labels = {
            'avatar': 'Аватар',
            'nickname': 'Никнейм',
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'birthday': 'Дата рождения',
            'email': 'Email',
        }
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'uploadFile img'}),
            'nickname': forms.TextInput(attrs={'class': 'field-update-form'}),
            'last_name': forms.TextInput(attrs={'class': 'field-update-form'}),
            'first_name': forms.TextInput(attrs={'class': 'field-update-form'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'field-update-form'}),
            'email': forms.TextInput(attrs={'class': 'field-update-form'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['nickname'].initial = self.instance.nickname
        self.fields['last_name'].initial = self.instance.last_name
        self.fields['first_name'].initial = self.instance.first_name
        self.fields['birthday'].initial = self.instance.birthday
        self.fields['email'].initial = self.instance.email
