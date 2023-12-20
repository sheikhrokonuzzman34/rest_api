from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('changepassword/', PasswordChangeAPIView.as_view(), name='change-password'),
    path('Update/', MyUserUpdateAPIView.as_view(), name='Update'),
    path('api/user/update/', MyUserUpdateAPIView.as_view(), name='user-update'),
]