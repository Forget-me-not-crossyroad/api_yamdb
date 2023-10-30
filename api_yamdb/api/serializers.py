from rest_framework import serializers
from reviews.models import Categories, Genres, Reviews, Comments, Titles
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import mixins
from rest_framework import viewsets

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


class TitlesSerializer(serializers.ModelSerializer):
    raiting = serializers.SerializerMethodField()
    category = SlugRelatedField(queryset=Categories.objects.all(),
                                slug_field='slug',
                                )
    genre = SlugRelatedField(queryset=Genres.objects.all(),
                             slug_field='slug',
                             many=True
                             )

    def get_raiting(self, title_object):
        raiting = title_object.reviews.all().aggregate(Avg('score'))['score__avg']
        if raiting:
            return int(raiting)
        return raiting

    class Meta:
        model = Titles
        fields = ('name', 'year', 'description', 'genre', 'category')


class CategoriesSerializer(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    name = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Titles
        fields = ('name', 'slug')


class GenresSerializer(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


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
