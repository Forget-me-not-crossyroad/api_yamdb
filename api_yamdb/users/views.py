from rest_framework.viewsets import ModelViewSet

from reviews.models import Users
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

