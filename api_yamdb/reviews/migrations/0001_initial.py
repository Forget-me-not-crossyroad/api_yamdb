import django.core.validators
import django.db.models.deletion
import reviews.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название категории (не более 256 символов)', max_length=256, verbose_name='Название')),
                ('slug', models.SlugField(help_text='Идентификатор страницы для URL (разрешены символы латиницы, цифры, дефис и подчёркивание.Не более 50 символов)', unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название категории (не более 256 символов)', max_length=256, verbose_name='Название')),
                ('slug', models.SlugField(help_text='Идентификатор страницы для URL (разрешены символы латиницы, цифры, дефис и подчёркивание.Не более 50 символов)', unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название произведения (не более 256 символов)', max_length=256, verbose_name='Название')),
                ('year', models.PositiveSmallIntegerField(help_text='Введите целочисленное значение года', validators=[reviews.validators.validate_year], verbose_name='Год выпуска')),
                ('description', models.TextField(blank=True, help_text='Текст описания произведения', verbose_name='Описание')),
                ('category', models.ForeignKey(help_text='Выберите категорию', null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.category', verbose_name='Внешний ключ таблицы категория')),
                ('genre', models.ManyToManyField(help_text='Выберите жанр произведения', related_name='titles', to='reviews.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'произведение',
                'verbose_name_plural': 'Произведения',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите текст отзыва', verbose_name='Текст')),
                ('score', models.IntegerField(help_text='Поставьте оценку от 1 до 10', validators=[django.core.validators.MinValueValidator(1, message='Минимальная оценка равна 1.'), django.core.validators.MaxValueValidator(10, message='Максимальная оценка равна 10.')], verbose_name='Оценка')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор отзыва')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title', verbose_name='Произведение')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.review', verbose_name='Отзыв')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='one_review'),
        ),
    ]
