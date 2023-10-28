from rest_framework import viewsets
from reviews.models import Titles
from .serializers import ReviewsSerializer, CommentsSerializer
from django.shortcuts import get_object_or_404


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Titles, pk=self.kwargs['title_id'])
        )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, pk=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        title=get_object_or_404(Titles, pk=self.kwargs['title_id'])
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(title.reviews, pk=self.kwargs['review_id'])
        )
