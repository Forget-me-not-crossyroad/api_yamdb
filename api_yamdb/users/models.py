from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from api_yamdb.constants import (MAX_LENGTH_BIO, MAX_LENGTH_EMAIL,
                                 MAX_LENGTH_ROLE)

USER_GROUPS = (
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin')
)


class Users(AbstractUser):

    email = models.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        unique=True
    )
    bio = models.CharField(
        max_length=MAX_LENGTH_BIO,
        blank=True
    )
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE,
        default='user',
        choices=USER_GROUPS,
        verbose_name='Группа пользователя',
        help_text='Одна из: user, moderator, admin'
    )

    @property
    def is_admin(self):
        return self.is_superuser or self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def clean(self):

        if self.role == 'me':
            raise ValidationError(
                {'username': '"me" не может быть именем пользователя.'})

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"
