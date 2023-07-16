import random
from typing import Dict
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import BlogPostForm
from .models import BlogPost
from account.utils import DataMixin, things


def get_header(header: str) -> Dict:
    header = header.split()
    index = len(header) // 2
    first = header[:index]
    second = header[index:]
    context = {'first': f'{" ".join(first).capitalize()}',
               'second': f'{" ".join(second).capitalize()}'}
    return context


class Posts(DataMixin, ListView):
    model = BlogPost
    template_name = 'blog_post/blog.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        header = get_header('Страницы из дневника')
        base_context = self.get_user_context(title='Страницы из дневника',
                                             header_first=header['first'],
                                             header_second=header['second'])
        return dict(list(context.items()) + list(base_context.items()))

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class CreatePost(DataMixin, LoginRequiredMixin, CreateView):
    template_name = 'blog_post/create_post.html'
    form_class = BlogPostForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        thing = random.choice(things)
        header = get_header('Новая страница')
        base_context = self.get_user_context(title='Новая страница',
                                             header_first=header['first'],
                                             header_second=header['second'],
                                             thing=thing)
        return dict(list(context.items()) + list(base_context.items()))

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        return super().form_valid(form)


class PostDetail(DataMixin, DetailView):
    model = BlogPost
    template_name = 'blog_post/blog-single.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        header = get_header(self.object.title)
        base_context = self.get_user_context(title=self.object.title,
                                             header_first=header['first'],
                                             header_second=header['second'])
        return dict(list(context.items()) + list(base_context.items()))


class UpdatePost(DataMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    template_name = 'blog_post/create_post.html'
    form_class = BlogPostForm
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        thing = random.choice(things)
        header = get_header(self.object.title)
        base_context = self.get_user_context(title=self.object.title,
                                             header_first=header['first'],
                                             header_second=header['second'],
                                             thing=thing)
        return dict(list(context.items()) + list(base_context.items()))

    def get_initial(self):
        data = BlogPost.objects.get(slug=self.kwargs.get('post_slug'))
        return {'title': data.title, 'text': data.text}

    def test_func(self):
        return self.get_object().author_id == self.request.user.pk


class DeletePost(UserPassesTestMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('posts:posts')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse('posts:posts')

    def test_func(self):
        return self.get_object().author_id == self.request.user.pk
