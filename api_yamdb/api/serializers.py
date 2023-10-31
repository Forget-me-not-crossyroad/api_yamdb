from rest_framework import serializers
from reviews.models import Categories, Genres, Reviews, Comments, Titles, Users
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import mixins
from rest_framework import viewsets
# from api.serializers import GenresSerializer, CategoriesSerializer

CATEGORIES_CHOICES = {'Фильмы', 'Книги', 'Музыка'}

CHOICES = (
          ('Фильмы', 'Films'),
          ('Книги', 'Books'),
          ('Музыка', 'Music'),
)

class CategoriesNameChoice(serializers.Field):

    def to_representation(self, value):
        return value
    def to_internal_value(self, data):
        if data not in CATEGORIES_CHOICES:
            raise serializers.ValidationError('Этой категории нет в списке')
        return data


class CategoriesSerializer(serializers.ModelSerializer):
    name = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Titles
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlesGetSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(queryset=Categories.objects.all(),
                                slug_field='slug',
                                )
    genre = SlugRelatedField(queryset=Genres.objects.all(),
                             slug_field='slug',
                             many=True
                             )

    class Meta:
        model = Titles
        fields = ('category', 'genre', 'name', 'year')


class TitlesWriteSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = CategoriesSerializer()
    genre = GenresSerializer(many=True)

    def get_rating(self, title_object):
        rating = title_object.reviews.all().aggregate(Avg('score'))['score__avg']
        if rating:
            return int(rating)
        return rating

    class Meta:
        model = Titles
        fields = ('name', 'year', 'rating', 'description', 'genre', 'category')


class ReviewsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Reviews
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        validators = [
            UniqueTogetherValidator(
                queryset=Reviews.objects.all(),
                fields=['title', 'author'],
                message=(
                    'Вы можете оставить только '
                    'один отзыв к этому произведению'
                )
            )
        ]


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
