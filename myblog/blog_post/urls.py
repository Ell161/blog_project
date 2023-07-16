from django.urls import path
from .views import *

app_name = 'posts'
urlpatterns = [
    path('', Posts.as_view(), name='posts'),
    path('new/', CreatePost.as_view(), name='new_post'),
    path('<slug:post_slug>/', PostDetail.as_view(), name='post-detail'),
    path('update/<slug:post_slug>/', UpdatePost.as_view(), name='update_post'),
    path('delete/<slug:post_slug>/', DeletePost.as_view(), name='delete_post'),
]
