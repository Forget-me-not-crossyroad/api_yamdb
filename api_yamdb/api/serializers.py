from rest_framework import serializers
from reviews.models import Categories, Genres, Reviews, Comments, Titles, Users
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg
from rest_framework.validators import UniqueTogetherValidator

CATEGORIES_CHOICES = {'Фильмы', 'Книги', 'Музыка'}

CHOICES = (
          ('Фильмы', 'Films'),
          ('Книги', 'Books'),
          ('Музыка', 'Music'),
)


class CategoriesSerializer(serializers.ModelSerializer):
    # name = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Categories
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitlesWriteSerializer(serializers.ModelSerializer):
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


class TitlesGetSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(
        read_only=True,
        many=True
    )

    def get_rating(self, title_object):
        rating = title_object.reviews.all().aggregate(Avg('score'))['score__avg']
        if rating:
            return int(rating)
        return rating

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class ReviewsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Reviews
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
