from django.views.generic import ListView
from .models import BlogPost


class Posts(ListView):
    model = BlogPost
    template_name = 'blog_post/blog.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = [{'title': 'MySecret', 'url_name': 'posts:posts'},
                           {'title': 'Добавить пост', 'url_name': 'posts:posts'},
                           {'title': 'Войти', 'url_name': 'posts:posts'}]
        context['title'] = 'Статьи'
        return context

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)
