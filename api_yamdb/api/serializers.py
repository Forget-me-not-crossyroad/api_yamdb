from rest_framework import serializers
from reviews.models import Category, Genre, Review, Comment, Title
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg

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
    rating = serializers.SerializerMethodField()
    category = CategoriesSerializer()
    genre = GenresSerializer(
        many=True
    )

    def get_rating(self, title_object):
        rating = title_object.reviews.all().aggregate(
            Avg('score'))['score__avg']
        if rating:
            return int(rating)
        return rating

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class ReviewsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id',)

    def validate(self, data):
        if (Review.objects.filter(
                author=self.context.get('request').user,
                title=self.context.get('view').kwargs.get('title_id')).exists()
                and self.context.get('request').method == 'POST'):
            raise serializers.ValidationError(
                'Вы можете оставить только один отзыв на произведение'
            )

        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
