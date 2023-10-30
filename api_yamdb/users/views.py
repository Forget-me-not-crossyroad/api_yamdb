from rest_framework.viewsets import ModelViewSet

from reviews.models import Users
from .serializers import UsersSerializer


class UserViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

