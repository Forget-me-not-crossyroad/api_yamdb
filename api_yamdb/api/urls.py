from rest_framework.routers import SimpleRouter
from .views import CategoriesViewSet, GenresViewSet, ReviewsViewSet, CommentsViewSet, TitlesViewSet
from django.urls import path, include

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

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    #path('v1/', include('djoser.urls.jwt')),
    # Эндпоинт для получения Token
]
