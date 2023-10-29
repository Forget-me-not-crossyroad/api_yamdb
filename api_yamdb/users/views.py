from rest_framework.viewsets import ModelViewSet

from reviews.models import Users, UserProfile
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

