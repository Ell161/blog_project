from django.urls import path
from .views import *

app_name = 'posts'
urlpatterns = [
    path('', Posts.as_view(), name='posts'),
    path('<int:id>/', PostDetail.as_view(), name='post-detail'),
    path('update/<int:id>/', UpdatePost.as_view(), name='update_post'),
    path('delete/<int:id>/', DeletePost.as_view(), name='delete_post'),
    path('new/', CreatePost.as_view(), name='new_post'),
]