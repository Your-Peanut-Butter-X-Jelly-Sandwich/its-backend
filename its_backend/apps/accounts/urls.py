from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    AddTutorStudentRelationshipView,
    ChangePasswordView,
    CustomSignupView,
    LoginView,
    LogoutView,
    PromoteStudentsView,
    RetrieveStudentsView,
    RetrieveTutorsView,
    RetrieveUserView,
    SignUpView,
    SocialCallbackView,
    UpdateUserInfoView,
)

urlpatterns = [
    path("auth/", include("allauth.urls")),
    path("auth/change-password", ChangePasswordView.as_view(), name="change_password"),
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/logout", LogoutView.as_view(), name="logout"),
    path("auth/signup", SignUpView.as_view(), name="signup"),
    path("auth/social", SocialCallbackView.as_view(), name="social_callback"),
    path(
        "auth/social/signup/", CustomSignupView.as_view(), name="socialaccount_signup"
    ),
    path("auth/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/update-info", UpdateUserInfoView.as_view(), name="update_info"),
    path("auth/user", RetrieveUserView.as_view(), name="retrieve_user"),
    path("students", RetrieveStudentsView.as_view(), name="retrieve_students"),
    path("students/promote", PromoteStudentsView.as_view(), name="promote_to_tutors"),
    path("tutors", RetrieveTutorsView.as_view(), name="retrieve_tutors"),
    path(
        "teaches",
        AddTutorStudentRelationshipView.as_view(),
        name="add_tutor_student_relationship",
    ),
]
