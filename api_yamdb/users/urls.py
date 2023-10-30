from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

users_router = DefaultRouter()

users_router.register('', UserViewSet, basename='MyUsers')

urlpatterns = [
    path('', include(users_router.urls)),
    # path('', send_confirmation_code, name='send_confirmation_code'), #'users/' GET, POST
    # path('<slug:username>/', obtain_token, name='obtain_token'), #username/ GET, PATCH, DELETE
    # path('me/', patch_user, name='patch_user'), #me/ GET, PATCH
    # path('', include(v1_router.urls)),
]