from django.urls import path, include
from .views import SignUpView, LoginView, LogoutView, CustomSignupView, SocialCallbackView, RetrieveUserView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (AddTutorStudentRelationshipView, ChangePasswordView, RetrieveStudentsView, RetrieveTutorsView)

urlpatterns = [
    path('auth/login', LoginView.as_view() , name='login'),
    path('auth/signup', SignUpView.as_view(), name='signup'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user', RetrieveUserView.as_view(), name='retrieve_user'),
    path('auth/social', SocialCallbackView.as_view(), name='social_callback'),
    path('auth/social/signup/', CustomSignupView.as_view(), name='socialaccount_signup' ),
    path('auth/', include('allauth.urls')),    
    path('auth/change-password', ChangePasswordView.as_view(), name='change_password'),
    # TODO: update API paths
    path('students', RetrieveStudentsView.as_view(), name='retrieve_students'),
    path('tutors', RetrieveTutorsView.as_view(), name='retrieve_tutors'),
    path('teaches', AddTutorStudentRelationshipView.as_view(), name='add_tutor_student_relationship')
]