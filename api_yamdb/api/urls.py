from rest_framework.routers import SimpleRouter
from django.urls import path, include

from .views import CategoriesViewSet, GenresViewSet, ReviewsViewSet, CommentsViewSet, TitlesViewSet
from users.views import UsersModelViewSet

router_v1 = SimpleRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router_v1.register('titles', TitlesViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register('categories', CategoriesViewSet)
router_v1.register('users', UsersModelViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
