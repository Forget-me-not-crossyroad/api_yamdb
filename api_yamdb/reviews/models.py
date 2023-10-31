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


class Users(AbstractUser):
    bio = models.CharField(max_length=500, null=True, blank=True)
    role = models.CharField(max_length=15,
                                blank=False,
                                default='user',
                                validators=[validate_profile_group],
                                verbose_name='Группа пользователя',
                                help_text='Одна из: user, moderator, admin')

    def __str__(self):
        return self.username


class Titles(models.Model):
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
        'Genres',
        through='GenreTitle',
        verbose_name='Внешний ключ таблицы жанр',
        help_text='Array of strings (Slug жанра)'
    )
    category = models.ForeignKey(
        'Categories',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Внешний ключ таблицы категория',
        help_text='string (Slug категории)'
    )

    def __str__(self):
        return self.name


class Categories(models.Model):
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


class Genres(models.Model):
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


class Reviews(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )
    text = models.TextField(
        'Текст'
    )
    author = models.OneToOneField(
        Users, on_delete=models.CASCADE,
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


class Comments(models.Model):
    rewiew = models.ForeignKey(
        Reviews,
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
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
