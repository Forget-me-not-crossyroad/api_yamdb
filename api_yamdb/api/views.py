from rest_framework import viewsets, mixins
from reviews.models import Category, Genre, Title
from .serializers import CategoriesSerializer, GenresSerializer, ReviewsSerializer, CommentsSerializer, TitlesWriteSerializer, TitlesGetSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import TitleFilter

class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        print(serializer)
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs['title_id'])
        )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, pk=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(title.reviews, pk=self.kwargs['review_id'])
        )


class TitlesViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Title."""

    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']

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
