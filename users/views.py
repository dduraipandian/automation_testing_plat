from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from users.utils import validate_user_email, validate_user_password, get_user_model


@login_required()
def home(request):
    if request.user.is_authenticated:
        response = render(request, 'home.html')
    else:
        response = redirect("/login/")
    return response


def logout(request):
    auth_logout(request)
    response = redirect("/login/")
    return response


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            auth_login(request, user)
            response = redirect("/")
        else:
            messages.error(request, 'Invalid login information.')
            response = render(request, 'login.html')
    elif request.method == 'GET' and request.user.is_authenticated:
        response = redirect("/")
    else:
        response = render(request, 'login.html')

    return response


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Email validation
        valid, err_response = validate_user_email(email)
        if not valid:
            messages.error(request, err_response)
            response = render(request, 'register.html')
            return response

        # Password validation
        valid, err_response = validate_user_password(password1, password2)
        if not valid:
            messages.error(request, err_response)
            response = render(request, 'register.html')
            return response
        else:
            password = password1

        if not name:
            messages.error(request, 'Name can not be empty')
            response = render(request, 'register.html')
            return response

        data = dict()
        data['email'] = email
        data['name'] = name
        data['password'] = password

        user = get_user_model()(**data)
        user.set_password(password)
        user.save()
        auth_login(request, user)
        response = render(request, 'home.html')
    else:
        response = render(request, 'register.html')

    return response
