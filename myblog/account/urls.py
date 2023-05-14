from django.urls import path
from .views import *

app_name = 'account'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password_change/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_change'),
]