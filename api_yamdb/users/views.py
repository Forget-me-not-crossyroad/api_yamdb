from api.mixins import UpdateModelMixin
from api.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UsersSerializer

Users = get_user_model()


class UserAccessesModel(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                        UpdateModelMixin, viewsets.GenericViewSet):
    pass


class UsersModelViewSet(UserAccessesModel):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminUser, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(self.request.user,
                                             many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @me.mapping.patch
    def patch_user(self, request):
        serializer = self.get_serializer(self.request.user,
                                         data=request.data,
                                         partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save(role=self.request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
