from django.db import models
from django.urls import reverse
from django.conf import settings


class BlogPost(models.Model):
    def post_directory_path(self, filename):
        return 'page_pictures/{0}/{1}/{2}'.format(self.author, self.pk, filename)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Содержание')
    timestamp = models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')
    page_picture = models.ImageField(upload_to=post_directory_path, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs={'id': self.pk})

    def save(self, *args, **kwargs):
        try:
            this = BlogPost.objects.get(id=self.pk)
            if this.page_picture != self.page_picture:
                this.page_picture.delete()
        except:
            pass
        picture, self.page_picture = self.page_picture, None
        super(BlogPost, self).save(*args, **kwargs)
        self.page_picture = picture
        super(BlogPost, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Страницы'
        verbose_name = 'Страница'
        ordering = ['-timestamp']

