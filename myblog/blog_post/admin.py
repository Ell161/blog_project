from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'timestamp', )
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text', )
    prepopulated_fields = {'slug': ('title',)}
