import functools
import re
from django.contrib.auth import get_user_model as user_model
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, URLValidator
from django.contrib.auth.password_validation import validate_password


@functools.lru_cache(maxsize=10)
def get_user_model():
    User = user_model()
    return User


def is_distinct_user(email):
    is_distinct = False
    try:
        get_user_model().objects.get(email=email)
    except Exception as e:
        is_distinct = True
    else:
        is_distinct = False

    return is_distinct


def validate_user_email(email):
    if not email:
        valid, msg = False, 'Email can not be empty.'
    else:
        try:
            validate_email(email)
        except ValidationError as e:
            valid, msg = False, 'Email is not valid.'
        else:
            valid, msg = True, None

        is_distinct = is_distinct_user(email)

        if not is_distinct:
            valid, msg = False, 'Email is already registered.'

    return valid, msg


def validate_user_password(password1, password2):
    if not (password1 and password1):
        valid, msg = False, 'password can not be empty.'
    elif password1 != password2:
        valid, msg = False, 'password does not match.'
    else:
        try:
            validate_password(password1)
        except ValidationError as e:
            error_message = "\n".join([m.message for m in e.error_list])
            valid, msg = False, error_message
        else:
            valid, msg = True, None
    return valid, msg
