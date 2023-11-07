from api.mixins import UpdateModelMixin
from api.permissions import UserPermissions
from django.shortcuts import get_object_or_404
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
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = get_object_or_404(Users, id=self.request.user.id)

        if request.method == 'GET':
            serializer = self.get_serializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':

            serializer = self.get_serializer(user,
                                             data=request.data,
                                             partial=True)

            if serializer.is_valid():
                if request.data.get('role') != user.role:
                    serializer.validated_data['role'] = user.role

                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            else:
                return Response(serializer.data,
                                status=status.HTTP_400_BAD_REQUEST)
