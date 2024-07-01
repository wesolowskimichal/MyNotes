from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views.user_view import *
from api.views.group_view import *


urlpatterns = [
    # User
    path('register/', UserRegisterView.as_view(), name='register'),
    path('user/', UserDetailsView.as_view(), name='user_operations'),
    # User Groups
    path('groups/', GroupView.as_view(), name='create_note_group'),
    # Token
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
]