from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import UsersSerializer

Users = get_user_model()


@csrf_exempt
@api_view(['POST'])
def send_confirmation_code(request):

    username = request.data.get('username')
    email = request.data.get('email')

    serializer = UsersSerializer(data={'username': username, 'email': email})

    if not serializer.is_valid():
        if not Users.objects.filter(username=username,
                                    email=email,
                                    is_active=True).exists():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer.save()

    token = default_token_generator.make_token(
        Users.objects.get(username=username))

    msg = EmailMessage(f'Код подтверждения для {username}.',
                       f'Ваш код подтверждения: {token}',
                       to=[email])
    msg.send()

    return Response({'email': email, 'username': username},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def obtain_token(request):

    if not request.data.get('username'):
        return Response({'username': ['Отсутствует поле username.'], },
                        status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(Users, username=request.data.get('username'))

    if not user:
        return Response({'username': ['Пользователь не найден'], },
                        status=HTTPStatus.NOT_FOUND)

    if default_token_generator.check_token(
            user,
            request.data.get('confirmation_code')
    ):
        refresh = RefreshToken.for_user(user)
        content = {'token': str(refresh.access_token), }
        return Response(content, status=status.HTTP_200_OK)
    else:
        return Response({'token': ['Неверный код подтверждения.'], },
                        status=status.HTTP_400_BAD_REQUEST)
