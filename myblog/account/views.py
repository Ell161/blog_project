from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from .forms import *
from blog_post.models import BlogPost
from .utils import DataMixin


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


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):  # Ошибка аргументов - исправить
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


class UserPostListView(DataMixin, ListView):
    model = BlogPost
    template_name = 'account/personal_page.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.request.user.pk)
        return BlogPost.objects.filter(author=user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_user_context(title='Личный кабинет')
        return dict(list(context.items()) + list(base_context.items()))


class UserUpdateInfo(DataMixin, UpdateView):
    context_object_name = 'variable_used_in `update.html`'
    form_class = UserUpdateForm
    template_name = 'account/personal_info_update.html'
    success_url = reverse_lazy('account:account')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        base_context = self.get_user_context(title='Личный кабинет')
        return dict(list(context.items()) + list(base_context.items()))

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
