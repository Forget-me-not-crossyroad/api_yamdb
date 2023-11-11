from datetime import date

from django.core.exceptions import ValidationError


def validate_year(value):
    if value > date.today().year:
        raise ValidationError(
            'Год не может быть больше текущего.'
        )
    return value
