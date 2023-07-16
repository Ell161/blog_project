from django.db import models
from django.urls import reverse, reverse_lazy
from django.conf import settings


class BlogPost(models.Model):
    def post_directory_path(self, filename):
        return 'page_pictures/{0}/{1}/{2}'.format(self.author, self.slug, filename)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    text = models.TextField(verbose_name='Содержание')
    timestamp = models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')
    page_picture = models.ImageField(upload_to=post_directory_path, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('posts:post-detail', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        try:
            this = BlogPost.objects.get(id=self.pk)
            if this.page_picture != self.page_picture:
                this.page_picture.delete()
        except:
            pass
        picture, self.page_picture = self.page_picture, None
        if not self.slug:
            self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)
        self.page_picture = picture
        super(BlogPost, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Страницы'
        verbose_name = 'Страница'
        ordering = ['-timestamp']
