from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    timestamp = models.DateField(auto_now=True)
    is_published = models.BooleanField(default=True)

