from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

Users = get_user_model()


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text=('Название произведения; не более 256 символов')
    )
    year = models.DateField(
        verbose_name='Год выпуска',
        help_text=('Год выпуска; целочисленное значение года')
    )
    description = models.TextField(
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
        on_delete=models.CASCADE,
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
        max_length=50,
        unique=True,
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
        max_length=50,
        unique=True,
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
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='one_review'
            ),
        )


class Comments(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='comments'
    )
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
