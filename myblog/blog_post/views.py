import random
from typing import Dict
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import BlogPostForm
from .models import BlogPost


def get_header(header: str) -> Dict:
    header = header.split()
    index = len(header) // 2
    first = header[:index]
    second = header[index:]
    context = {'first': f'{" ".join(first).capitalize()}',
               'second': f'{" ".join(second).capitalize()}'}
    return context


class Posts(ListView):
    model = BlogPost
    template_name = 'blog_post/blog.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_auth'] = [{'title': 'MySecret', 'url_name': 'posts:posts'},
                                {'title': 'Новая страница', 'url_name': 'posts:new_post'},
                                {'title': 'Личный кабинет', 'url_name': 'account:account'},
                                {'title': 'Выйти', 'url_name': 'account:logout'}]
        context['menu_not_auth'] = [{'title': 'MySecret', 'url_name': 'posts:posts'},
                                    {'title': 'Новая страница', 'url_name': 'posts:new_post'},
                                    {'title': 'Войти', 'url_name': 'account:login'}]
        context['title'] = 'Страницы из дневника'
        header = get_header(context['title'])
        context['header_first'] = header['first']
        context['header_second'] = header['second']
        return context

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class CreatePost(LoginRequiredMixin, CreateView):
    template_name = 'blog_post/create_post.html'
    form_class = BlogPostForm
    things = ['От счастья до депрессии – одна мысль. (Б. Спиноза)',
              'Душа, в отличие от разума, не думает и не рассуждает — она чувствует и знает, поэтому не ошибается.',
              'Навязчивые мысли грызут так же упорно, как неизлечимые болезни. Внедрившись однажды в душу, '
              'они пожирают ее, не дают ни о чем думать, ничем интересоваться. (Ги де Мопассан)',
              'Столько есть всего, о чём надо подумать. Зачем забивать себе голову тем, чего уже не вернёшь, '
              '— надо думать о том, что ещё можно изменить. (Маргарет Митчелл)',
              '— Почему ты все время думаешь? — Потому что мир в моей голове интереснее, чем этот.',
              'Она вовсе не выбирала его. Просто ни о ком другом она не думала...']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = [{'title': 'MySecret', 'url_name': 'posts:posts'},
                           {'title': 'Личный кабинет', 'url_name': 'account:account'},
                           {'title': 'Выйти', 'url_name': 'account:logout'}]
        context['title'] = 'Новая страница'
        header = get_header(context['title'])
        context['header_first'] = header['first']
        context['header_second'] = header['second']
        context['thing'] = random.choice(self.things)
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('posts:post-detail', kwargs={'id': self.object.pk})


class PostDetail(DetailView):
    model = BlogPost
    template_name = 'blog_post/blog-single.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_auth'] = [{'title': 'MySecret', 'url_name': 'posts:posts'},
                                {'title': 'Новая страница', 'url_name': 'posts:new_post'},
                                {'title': 'Личный кабинет', 'url_name': 'account:account'},
                                {'title': 'Выйти', 'url_name': 'account:logout'}]
        context['menu_not_auth'] = [{'title': 'MySecret', 'url_name': 'posts:posts'},
                                    {'title': 'Новая страница', 'url_name': 'posts:new_post'},
                                    {'title': 'Войти', 'url_name': 'account:login'}]
        context['title'] = self.object.title
        header = get_header(context['title'])
        context['header_first'] = header['first']
        context['header_second'] = header['second']
        return context


class UpdatePost(UserPassesTestMixin, UpdateView):
    model = BlogPost
    template_name = 'blog_post/create_post.html'
    form_class = BlogPostForm
    pk_url_kwarg = 'id'
    things = ['От счастья до депрессии – одна мысль. (Б. Спиноза)',
              'Душа, в отличие от разума, не думает и не рассуждает — она чувствует и знает, поэтому не ошибается.',
              'Навязчивые мысли грызут так же упорно, как неизлечимые болезни. Внедрившись однажды в душу, '
              'они пожирают ее, не дают ни о чем думать, ничем интересоваться. (Ги де Мопассан)',
              'Столько есть всего, о чём надо подумать. Зачем забивать себе голову тем, чего уже не вернёшь, '
              '— надо думать о том, что ещё можно изменить. (Маргарет Митчелл)',
              '— Почему ты все время думаешь? — Потому что мир в моей голове интереснее, чем этот.',
              'Она вовсе не выбирала его. Просто ни о ком другом она не думала...',
              'Не ждите. Время никогда не будет подходящим.',
              'Служба поддержки текущей действительности у аппарата. Какие иллюзии вам требуется развеять?',
              'Есенин писал: "Своею гордою душою, прошел я счастье стороной"...задумайтесь.']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_auth'] = [{'title': 'MySecret', 'url_name': 'posts:posts'},
                                {'title': 'Новая страница', 'url_name': 'posts:new_post'},
                                {'title': 'Личный кабинет', 'url_name': 'account:account'},
                                {'title': 'Выйти', 'url_name': 'account:logout'}]
        context['menu_not_auth'] = [{'title': 'MySecret', 'url_name': 'posts:posts'},
                                    {'title': 'Новая страница', 'url_name': 'posts:new_post'},
                                    {'title': 'Войти', 'url_name': 'account:login'}]
        context['title'] = 'Новая страница'
        header = get_header(context['title'])
        context['header_first'] = header['first']
        context['header_second'] = header['second']
        context['thing'] = random.choice(self.things)
        return context

    def get_initial(self):
        data = BlogPost.objects.get(pk=self.kwargs.get('id'))
        return {'title': data.title, 'text': data.text}

    def get_success_url(self) -> str:
        return reverse('posts:post-detail', kwargs={'id': self.object.pk})

    def test_func(self):
        return self.get_object().author_id == self.request.user.pk


class DeletePost(UserPassesTestMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('posts:posts')
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse('posts:posts')

    def test_func(self):
        return self.get_object().author_id == self.request.user.pk

