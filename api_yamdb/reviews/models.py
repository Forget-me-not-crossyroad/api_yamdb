import re
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


USER_GROUPS = ['user', 'moderator', 'admin']


def validate_profile_group(value):
    if value in USER_GROUPS:
        return value
    else:
        raise ValidationError('Некорректная группа пользователя.')


def validate_user_name(value):
    if (re.fullmatch(r'^[\w.@+-]+\Z', value)):
        return value
    else:
        raise ValidationError("Некорректное имя пользователя")


def validate_email(value):
    if (len(value) == 0 or
            len(value) > 254 or
            not re.fullmatch(
                r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$',
                value)):
        raise ValidationError("Некорректное имя пользователя")


class Users(AbstractUser):
    username = models.CharField(max_length=150,
                                blank=False,
                                unique=True,
                                validators=[validate_user_name])
    email = models.EmailField(max_length=254,
                              blank=False,
                              unique=True,
                              validators=[validate_user_name])
    first_name = models.CharField(max_length=150,
                                  blank=True)
    last_name = models.CharField(max_length=150,
                                 blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    role = models.CharField(max_length=15,
                                blank=False,
                                default='user',
                                validators=[validate_profile_group],
                                verbose_name='Группа пользователя',
                                help_text='Одна из: user, moderator, admin')

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text=('Название категории; не более 256 символов')
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены символы'
                   ' латиницы, цифры, дефис и подчёркивание.'
                   'Не более 50символов')
    )


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text=('Название категории; не более 256 символов')
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены символы'
                   ' латиницы, цифры, дефис и подчёркивание.'
                   'Не более 50символов')
    )

class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text=('Название произведения; не более 256 символов')
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        help_text=('Год выпуска; целочисленное значение года')
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Текст описания произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Внешний ключ таблицы категория',
        help_text='string (Slug категории)'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )
    text = models.TextField(
        'Текст'
    )
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        related_name='reviews'
    )
    score = models.IntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "Отзывы"
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='one_review'
            ),
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        auto_now_add=True
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
