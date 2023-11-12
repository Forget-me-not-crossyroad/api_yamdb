from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Genre, Title

from .filters import TitleFilter
from .mixins import UpdateModelMixin
from .permissions import CommonTopicsPermissions, ContentPermissions
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, ReviewsSerializer,
                          TitlesGetSerializer, TitlesWriteSerializer)


class ReviewsViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ReviewsSerializer
    permission_classes = (ContentPermissions,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs['title_id'])
        )


class CommentsViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CommentsSerializer
    permission_classes = (ContentPermissions,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, pk=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(title.reviews,
                                     pk=self.kwargs['review_id'])
        )


class TitlesViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    UpdateModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для модели Title."""

    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (CommonTopicsPermissions, )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesGetSerializer
        return TitlesWriteSerializer


class CategoriesViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """ViewSet для модели Categories."""

    queryset = Category.objects.all()
    lookup_field = "slug"
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    permission_classes = (CommonTopicsPermissions, )


class GenresViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """ViewSet для модели Categories."""

    queryset = Genre.objects.all()
    search_fields = ('name',)
    lookup_field = "slug"
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    permission_classes = (CommonTopicsPermissions, )
