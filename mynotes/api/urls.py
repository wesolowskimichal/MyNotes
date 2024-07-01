from django.urls import path
from api.views.user_view import *


urlpatterns = [
    path('user/register', UserRegisterView.as_view(), name='register')
]