from rest_framework.serializers import ModelSerializer
from reviews.models import Users


class UsersSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'bio')
