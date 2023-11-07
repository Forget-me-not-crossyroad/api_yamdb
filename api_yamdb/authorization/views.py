import re
from http import HTTPStatus

from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Users


def provide_password(exist, username, mail):

    pwd = Users.objects.make_random_password()
    if exist:
        u = Users.objects.get(username=username, is_active=True)
        u.set_password(pwd)
        u.save()
    else:
        Users.objects.create_user(username, mail, pwd)

    return pwd


@csrf_exempt
@api_view(['POST'])
def send_confirmation_code(request):

    profile = request.data.get('username')
    mail = request.data.get('email')

    if not profile:
        return Response(
            {'email': [], 'username': ['Отсутствует поле.']},
            status=status.HTTP_400_BAD_REQUEST)
    elif (len(profile) == 0 or len(profile) > 150 or profile == 'me'
          or not re.fullmatch(
              r'^[a-zA-Z0-9_.+-]+$',
              profile)):
        return Response(
            {'email': [], 'username': ['Некорректное поле.']},
            status=status.HTTP_400_BAD_REQUEST)

    if not mail:
        return Response({'email': ['Отсутствует поле.'], 'username': []},
                        status=status.HTTP_400_BAD_REQUEST)
    elif (len(mail) == 0 or len(mail) > 254
          or not re.fullmatch(
              r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$',
              mail)):
        return Response(
            {'email': ['Некорректный email.'], 'username': []},
            status=status.HTTP_400_BAD_REQUEST)

    if (Users.objects.filter(email=mail, is_active=True)
            .exclude(username=profile).exists()):
        return Response(
            {'email': ['Некорректный email.'], 'username': []},
            status=status.HTTP_400_BAD_REQUEST)

    if Users.objects.filter(username=profile,
                            email=mail,
                            is_active=True).exists():
        pwd = provide_password(True, profile, mail)
    elif Users.objects.filter(username=profile, is_active=True).exists():
        return Response(
            data={'username': [f'Пользователь {profile} уже существует.']},
            status=status.HTTP_400_BAD_REQUEST)
    else:
        pwd = provide_password(False, profile, mail)

    msg = EmailMessage(f'Код подтверждения для {profile}.',
                       f'Ваш код подтверждения: {pwd}',
                       to=[mail])
    msg.send()

    return Response({'email': mail, 'username': profile},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def obtain_token(request):

    if not request.data.get('username'):
        return Response({'username': ['Отсутствует поле username.'], },
                        status=status.HTTP_400_BAD_REQUEST)

    user = Users.objects.filter(username=request.data.get('username'),
                                is_active=True).first()

    if not user:
        return Response({'username': ['Пользователь не найден'], },
                        status=HTTPStatus.NOT_FOUND)

    if user.check_password(request.data.get('confirmation_code')):
        refresh = RefreshToken.for_user(user)
        content = {'token': str(refresh.access_token), }
        return Response(content, status=status.HTTP_200_OK)
    else:
        return Response({'password': ['Неверный пароль.'], },
                        status=status.HTTP_400_BAD_REQUEST)
