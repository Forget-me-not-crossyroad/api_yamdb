from rest_framework.serializers import ModelSerializer
from django.db import models

from reviews.models import Users


class UsersSerializer(ModelSerializer):
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(unique=False, max_length=150)
    last_name = models.CharField(unique=False, max_length=150)
    email = models.CharField(unique=True, max_length=254)

    class Meta:
        model = Users
        lookup_field = 'username'
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')
