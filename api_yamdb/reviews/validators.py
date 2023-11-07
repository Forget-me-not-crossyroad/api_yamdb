import re
from datetime import date

from django.core.exceptions import ValidationError

USER_GROUPS = ('user', 'moderator', 'admin')

def validate_year(value):
    if value > date.today().year:
        raise ValidationError(
            'Год не может быть больше текущего.'
        )
    return value


def validate_profile_group(value):
    if value in USER_GROUPS:
        return value
    raise ValidationError(
        'Некорректная группа пользователя.'
    )


def validate_user_name(value):
    if (re.fullmatch(r'^[\w.@+-]+\Z', value)):
        return value
    raise ValidationError(
        'Некорректное имя пользователя'
    )


def validate_email(value):
    if (len(value) == 0 or len(value) > 254
        or not re.fullmatch(
            r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$',
            value
        )
    ):
        raise ValidationError(
            'Некорректное имя пользователя'
        )
