from django.urls import path

from .views import obtain_token, send_confirmation_code

name = 'auth'

urlpatterns = [
    path('signup/', send_confirmation_code, name='send_confirmation_code'),
    path('token/', obtain_token, name='obtain_token'),
]
