from django.views.generic import TemplateView
from django.urls import path
from users.views import change_password, user_info

urlpatterns = [
    path('change_password/', change_password, name='change_password'),
    path('user_info/', user_info, name='user_info'),
]
