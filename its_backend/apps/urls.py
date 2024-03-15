from django.urls import include, path

urlpatterns = [
    path("", include("its_backend.apps.accounts.urls")),
    path("", include("its_backend.apps.submissions.urls")),
    path("", include("its_backend.apps.questions.urls")),
]
