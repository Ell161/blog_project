from django.urls import path
from .views import *

app_name = 'posts'
urlpatterns = [
    path('', Posts.as_view(), name='posts'),
    path('<int:id>/', PostDetail.as_view(), name='post-detail'),
    path('new/', CreatePost.as_view(), name='new_post'),
]