from rest_framework import serializers
from reviews.models import Reviews, Comments, Titles
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg
from rest_framework.validators import UniqueTogetherValidator

CATEGORIES_CHOICES = {'Фильмы', 'Книги', 'Музыка'}

class CategoriesNameChoice(serializers.Field):

    def to_representation(self, value):
        return value
    def to_internal_value(self, data):
        if data not in CATEGORIES_CHOICES:
            raise serializers.ValidationError('Этой категории нет в списке')
        return data


class TitlesSerializer(serializers.ModelSerializer):
    raiting = serializers.SerializerMethodField()
    category = CategoriesNameChoice()

    def get_raiting(self, title_object):
        raiting = title_object.reviews.all().aggregate(Avg('score'))['score__avg']
        if raiting:
            return int(raiting)
        return raiting

    class Meta:
        model = Titles
        fields = '__all__'


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
