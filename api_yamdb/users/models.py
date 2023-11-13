from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from api_yamdb.constants import (MAX_LENGTH_BIO, MAX_LENGTH_EMAIL,
                                 MAX_LENGTH_ROLE)

ADMIN_USER = 'admin'
DEFAULT_USER = 'user'
MODERATOR_USER = 'moderator'

USER_GROUPS = (
    (DEFAULT_USER, 'User'),
    (MODERATOR_USER, 'Moderator'),
    (ADMIN_USER, 'Admin')
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
        default=DEFAULT_USER,
        choices=USER_GROUPS,
        verbose_name='Группа пользователя',
        help_text=f'Одна из: {DEFAULT_USER}, {MODERATOR_USER}, {ADMIN_USER}'
    )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self):
        return self.is_superuser or self.role == ADMIN_USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR_USER

    def clean(self):
        if self.username == 'me':
            raise ValidationError(
                {'username': '"me" не может быть именем пользователя.'})
        super().clean()
