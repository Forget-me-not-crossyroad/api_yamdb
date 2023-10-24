from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

Users = get_user_model()


class Titles(models.Model):
    pass


class Categories(models.Model):
    pass


class Genres(models.Model):
    pass


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
