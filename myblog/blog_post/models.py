from django.db import models
from django.urls import reverse
from django.conf import settings


class BlogPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Содержание')
    timestamp = models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs={'id': self.pk})

    class Meta:
        verbose_name_plural = 'Страницы'
        verbose_name = 'Страница'
        ordering = ['-timestamp']

