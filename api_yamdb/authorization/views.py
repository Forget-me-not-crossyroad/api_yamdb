from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

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

    if Users.objects.filter(username=profile, email=mail, is_active=True).exists():
        pwd = provide_password(True, profile, mail)
    elif Users.objects.filter(username=profile, is_active=True).exists():
        return JsonResponse(data={'username': f'Пользователь {profile} уже существует.'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        pwd = provide_password(False, profile, mail)

    msg = EmailMessage(f'Код подтверждения для {profile}.',
                       f'Ваш код подтверждения: {pwd}',
                       to=[mail])

    print(f'Убрать заглушку в authorization/views для отправки сообщения на почту - Ваш код подтверждения: {pwd}')
    # msg.send()

    return JsonResponse(data={}, status=status.HTTP_200_OK)


@api_view(['POST'])
def obtain_token(request):

    user = get_object_or_404(Users, username=request.data.get('username'), is_active=True)

    if user.check_password(request.data.get('confirmation_code')):
        refresh = RefreshToken.for_user(user)
        content = {'token': str(refresh.access_token),}
        return Response(content, status=status.HTTP_200_OK)
    else:
        content = {'field_name': 'Неверный пароль.', }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
