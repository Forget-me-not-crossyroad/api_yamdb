from django.urls import path

from .views import send_confirmation_code, obtain_token

name = 'auth'

urlpatterns = [
    path('', send_confirmation_code, name='send_confirmation_code'),
    path('signup/', send_confirmation_code, name='send_confirmation_code'),
    path('token/', obtain_token, name='obtain_token'),
]
