from django.urls import path, include

urlpatterns = [
    path("", include("its_backend.apps.accounts.urls")),
    path("", include("its_backend.apps.submissions.urls")),
    path("", include("its_backend.apps.questions.urls")),
]
