from django.urls import path, include
from .views import SignUpView, LoginView, LogoutView, SocialCallbackView, RetrieveUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/login', LoginView.as_view() , name='login'),
    path('auth/signup', SignUpView.as_view(), name='signup'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/social', SocialCallbackView.as_view(), name='social_callback'),
    path('auth/user', RetrieveUserView.as_view(), name='retrieve_user'),
    path('auth/', include('allauth.urls')),    
]