from django.contrib.auth import get_user_model
from rest_framework import serializers


Users = get_user_model()


class UsersSerializer(serializers.ModelSerializer):

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
