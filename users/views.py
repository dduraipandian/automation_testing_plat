from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from users.utils import validate_user_email, validate_user_password, get_user_model
from automated_testing.views import get_all_published_articles


@login_required()
def home(request):
    if request.user.is_authenticated:
        articles = get_all_published_articles()
        response = render(request, 'home.html', {'articles': articles})
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


@require_http_methods(['GET', 'POST'])
@login_required(login_url='/login/')
def user_info(request):
    template = 'user_details.html'
    if request.method == 'POST':
        name = request.POST.get('name')
        user = request.user
        user.name = name
        try:
            user.save()
        except Exception as e:
            messages.error(request, 'Not able to update the information.')
            response = render(request, template)
        else:
            messages.success(request, 'Updated successfully.')
            response = render(request, template)
    elif request.method == 'GET' and request.user.is_authenticated:
        response = render(request, template)
    else:
        response = redirect("/")

    return response


@login_required(login_url='/login/')
@require_http_methods(['GET', 'POST'])
def change_password(request):
    template = 'user_details.html'
    if request.method == 'POST':
        try:
            user = request.user
            current_password = request.POST['password']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            validated_password = user.check_password(current_password)

            if not validated_password:
                messages.error(request, 'Current password is incorrect.!')
                response = render(request, template)
                return response

            # Password validation
            valid, err_response = validate_user_password(password1, password2)
            if not valid:
                messages.error(request, err_response)
                response = render(request, template)
                return response
            else:
                password = password1

            user.set_password(password)
            user.save()
            logout(request)
        except Exception as e:
            messages.error(request, 'Not able to update the information.')
            response = render(request, template)
        else:
            messages.success(request, 'Password updated successfully. Please re-login.')
            response = redirect("/")
    elif request.method == 'GET' and request.user.is_authenticated:
        response = render(request, template)
    else:
        response = redirect("/")

    return response
