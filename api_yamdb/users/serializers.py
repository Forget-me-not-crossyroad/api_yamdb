from rest_framework.serializers import ModelSerializer
from rest_framework.relations import SlugRelatedField

from reviews.models import Users, UserProfile


class UserSerializer(ModelSerializer):
    class Meta:
        model = Users, UserProfile
        fields = ('username', 'password', 'token')
