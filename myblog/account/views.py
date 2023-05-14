from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *


class UserLoginView(LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse_lazy('posts:posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        context['button'] = 'Войти'
        context['reset'] = 'Забыли пароль?'
        return context


class UserLogoutView(LogoutView):
    next_page = 'posts:posts'


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Changing the user's password.
    """
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html'
    success_message = "Мы отправили вам по электронной почте инструкции для сброса пароля, " \
                      "если учетная запись с указанным адресом электронной почты активна, " \
                      "вы получите письмо в ближайшее время."
    success_url = reverse_lazy('posts:posts')
    from_email = 'ev.chepiga.it@yandex.ru'
    extra_context = {'title': 'Сброс пароля'}
    extra_email_context = {'product': 'MySecret'}
    form_class = UserPasswordResetForm


#    def get_success_url(self):
#        return reverse_lazy('profile_detail', kwargs={'slug': self.request.user.profile.slug})


class ResetPasswordConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('posts:posts')
    success_message = "Пароль был успешно изменен!"
    extra_context = {'title': 'Изменение пароля'}
    form_class = UserPasswordChangeForm


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'account/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('posts:posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['button'] = 'Сохранить'
        context['reset'] = ''
        return context
