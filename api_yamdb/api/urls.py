from authorization.views import obtain_token, send_confirmation_code
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from users.views import UsersModelViewSet

from .views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                    ReviewsViewSet, TitlesViewSet)

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
router_v1.register('titles', TitlesViewSet,
                   basename='titles')
router_v1.register('genres', GenresViewSet,
                   basename='genres')
router_v1.register('categories', CategoriesViewSet,
                   basename='categories')
router_v1.register('users', UsersModelViewSet,
                   basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', send_confirmation_code,
         name='send_confirmation_code'),
    path('v1/auth/token/', obtain_token,
         name='obtain_token'),
]
