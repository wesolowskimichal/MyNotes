from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views.user_view import *
from api.views.group_view import *
from api.views.note_view import *


urlpatterns = [
    # User
    path('register/', UserRegisterView.as_view(), name='register'),
    path('user/', UserDetailsView.as_view(), name='user_operations'),
    path('user/contacts/', UserContactListView.as_view(), name='user_contacts'),
    path('user/contacts/invite/', UserContactsInvite.as_view(), name='user_contacts_invite'),
    # User Notes
    path('notes/', NoteView.as_view(), name='create_note'),
    path('notes/owned/', OwnedNoteView.as_view(), name='owned_notes'),
    # User Groups
    path('groups/', GroupListView.as_view(), name='group_operations'),
    path('groups/<uuid:id>/', GroupDetailsView.as_view(), name='group_details'),
    # Token
    path('token/', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
]