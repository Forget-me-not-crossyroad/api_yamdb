from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title

from .default_values import CurrentTitleDefault

CATEGORIES_CHOICES = {'Фильмы', 'Книги', 'Музыка'}

CHOICES = (
          ('Фильмы', 'Films'),
          ('Книги', 'Books'),
          ('Музыка', 'Music'),
)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'category', 'genre', 'name', 'year', 'description')

    def to_representation(self, instance):
        return TitlesGetSerializer(instance).data


class TitlesGetSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    category = CategoriesSerializer()
    genre = GenresSerializer(
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class ReviewsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        queryset=Users.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=CurrentTitleDefault())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('id', )
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author'],
                message='Вы можете оставить только один отзыв на произведение'
            )
        ]


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
