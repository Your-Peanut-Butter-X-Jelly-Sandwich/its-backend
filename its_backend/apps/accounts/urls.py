from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (ChangePasswordView, LoginView, LogoutView,
                    RetrieveUserView, SignUpView, SocialCallbackView)

urlpatterns = [
    path('auth/login', LoginView.as_view() , name='login'),
    path('auth/signup', SignUpView.as_view(), name='signup'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/social', SocialCallbackView.as_view(), name='social_callback'),
    path('auth/user', RetrieveUserView.as_view(), name='retrieve_user'),
    path('auth/change-password', ChangePasswordView.as_view(), name='change_password'),
    path('auth/', include('allauth.urls')),
]