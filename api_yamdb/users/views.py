from api.mixins import UpdateModelMixin
from api.permissions import UserPermissions
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UsersSerializer
from reviews.models import Users


class UsersModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
    permission_classes = (UserPermissions, )
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

        if serializer.is_valid(raise_exception=True):
            serializer.save(role=self.request.user.role)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
