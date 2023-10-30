from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import (SlugRelatedField,
                                        StringRelatedField,
                                        PrimaryKeyRelatedField,
                                        HyperlinkedRelatedField,
                                        RelatedField)

from reviews.models import Users, UserProfile


# class ProfileSerializer(ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ('role', 'bio')


class UserSerializer(ModelSerializer):
    role = SlugRelatedField(read_only=True, slug_field='role')

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'email', 'role')

        # username = RelatedField(read_only=True)

        # role = SlugRelatedField(read_only=True, slug_field='role')
        # bio = SlugRelatedField(read_only=True, slug_field='bio')
        # email = PrimaryKeyRelatedField(read_only=True)

        # fields = ['username', 'first_name', 'last_name', 'email', 'role', 'bio']
