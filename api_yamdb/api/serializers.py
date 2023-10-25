from rest_framework import serializers
from .models import Reviews, Comments, Titles
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg
from rest_framework.validators import UniqueTogetherValidator

class TitlesSerializer(serializers.ModelSerializer):
    raiting = serializers.SerializerMethodField()

    def get_raiting(self, title_object):
        title_object.reviews.all().aggregate(Avg('score'))['score__avg']

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
