from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


Users = get_user_model()


class UsersSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
