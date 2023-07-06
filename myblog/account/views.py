from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import request
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from .forms import *
from blog_post.models import BlogPost


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


class ResetPasswordView(SuccessMessageMixin, PasswordResetView): #Ошибка аргументов - исправить
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


class UserPostListView(ListView):
    model = BlogPost
    template_name = 'account/personal_page.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.request.user.pk)
        return BlogPost.objects.filter(author=user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_auth'] = [{'title': 'MySecret', 'url_name': 'posts:posts'},
                                {'title': 'Новая страница', 'url_name': 'posts:new_post'},
                                {'title': 'Выйти', 'url_name': 'account:logout'}]
        context['menu_not_auth'] = [{'title': 'MySecret', 'url_name': 'posts:posts'},
                                    {'title': 'Новая страница', 'url_name': 'posts:new_post'},
                                    {'title': 'Войти', 'url_name': 'account:login'}]
        context['title'] = 'Личный кабинет'
        return context


class UserUpdateInfo(UpdateView):
    context_object_name = 'variable_used_in `update.html`'
    form_class = UserUpdateForm
    template_name = 'account/personal_info_update.html'
    success_url = reverse_lazy('account:account')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_auth'] = [{'title': 'MySecret', 'url_name': 'posts:posts'},
                                {'title': 'Новая страница', 'url_name': 'posts:new_post'},
                                {'title': 'Личный кабинет', 'url_name': 'account:account'},
                                {'title': 'Выйти', 'url_name': 'account:logout'}]
        context['menu_not_auth'] = [{'title': 'MySecret', 'url_name': 'posts:posts'},
                                    {'title': 'Новая страница', 'url_name': 'posts:new_post'},
                                    {'title': 'Войти', 'url_name': 'account:login'}]
        context['title'] = 'Личный кабинет'
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        image = form.cleaned_data['avatar']
        print(image)
        if image:
            user.avatar = image
            user.save()
        return super().form_valid(form)
