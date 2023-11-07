from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from . import validators
from api_yamdb.constants import (MAX_LENGTH, MAX_LENGTH_BIO, MAX_LENGTH_EMAIL,
                                 MAX_LENGTH_NAME, MAX_LENGTH_ROLE)


class Users(AbstractUser):
    username = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=False,
        unique=True,
        validators=[validators.validate_user_name]
    )
    email = models.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        blank=False,
        unique=True,
        validators=[validators.validate_user_name]
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=True
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=True
    )
    bio = models.CharField(
        max_length=MAX_LENGTH_BIO,
        null=True,
        blank=True
    )
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE,
        blank=False,
        default='user',
        validators=[validators.validate_profile_group],
        verbose_name='Группа пользователя',
        help_text='Одна из: user, moderator, admin'
    )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название',
        help_text=('Название категории (не более 256 символов)')
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL (разрешены символы'
                   ' латиницы, цифры, дефис и подчёркивание.'
                   'Не более 50 символов)')
    )

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название',
        help_text=('Название категории (не более 256 символов)')
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL (разрешены символы'
                   ' латиницы, цифры, дефис и подчёркивание.'
                   'Не более 50 символов)')
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название',
        help_text='Название произведения (не более 256 символов)'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=[validators.validate_year],
        help_text='Введите целочисленное значение года'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Текст описания произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Выберите жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Внешний ключ таблицы категория',
        help_text='Выберите категорию'
    )

    class Meta:
        verbose_name = "произведение"
        verbose_name_plural = "Произведения"

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
        'Текст',
        help_text='Введите текст отзыва'
    )
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        related_name='reviews'
    )
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(
                1,
                message='Минимальная оценка равна 1.'
            ),
            MaxValueValidator(
                10,
                message='Максимальная оценка равна 10.'
            )
        ],
        help_text='Поставьте оценку от 1 до 10'
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

    def __str__(self):
        return self.text


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

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text
