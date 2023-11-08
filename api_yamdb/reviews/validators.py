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
