import random
from typing import Dict
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from .forms import BlogPostForm
from .models import BlogPost


def get_header(header: str) -> Dict:
    header = header.split()
    index = len(header) // 2
    first = header[:index]
    second = header[index:]
    context = {'first': f'{" ".join(first)}',
               'second': f'{" ".join(second).capitalize()}'}
    return context


class Posts(ListView):
    model = BlogPost
    template_name = 'blog_post/blog.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        context['menu'] = [{'title': 'MySecret', 'url_name': 'posts:posts'},
                           {'title': 'Добавить пост', 'url_name': 'posts:new_post'},
                           {'title': 'Войти', 'url_name': 'posts:posts'}]
        context['title'] = 'Страницы из дневника'
        header = get_header(context['title'])
        context['header_first'] = header['first']
        context['header_second'] = header['second']
        return context

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class CreatePost(CreateView):
    template_name = 'blog_post/create_post.html'
    form_class = BlogPostForm
    success_url = reverse_lazy('posts:posts')
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
                           {'title': 'Личный кабинет', 'url_name': 'posts:new_post'},
                           {'title': 'Выход', 'url_name': 'posts:posts'}]
        context['title'] = 'Новая страница'
        header = get_header(context['title'])
        context['header_first'] = header['first']
        context['header_second'] = header['second']
        context['thing'] = random.choice(self.things)
        return context


class PostDetail(DetailView):
    model = BlogPost
    template_name = 'blog_post/blog-single.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = [{'title': 'MySecret', 'url_name': 'posts:posts'},
                           {'title': 'Добавить пост', 'url_name': 'posts:new_post'},
                           {'title': 'Войти', 'url_name': 'posts:posts'}]
        context['title'] = self.object.title
        header = get_header(context['title'])
        context['header_first'] = header['first']
        context['header_second'] = header['second']
        return context
