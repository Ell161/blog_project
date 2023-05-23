from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, nickname, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, nickname, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(nickname, email, password, **extra_fields)


class User(AbstractUser):
    def user_directory_path(self, filename):
        return 'avatars/user_{0}/{1}'.format(self.pk, filename)

    username = None
    ordering = ('email',)

    email = models.EmailField(_('email address'), blank=False, unique=True)
    nickname = models.CharField(_('nickname'), max_length=30, blank=False, unique=True)
    last_name = models.CharField(_('surname'), max_length=30, blank=True)
    first_name = models.CharField(_('name'), max_length=30, blank=True)
    birthday = models.DateField(_("birthday"), blank=True, null=True)
    avatar = models.ImageField(_("avatar"), upload_to=user_directory_path, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', ]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
