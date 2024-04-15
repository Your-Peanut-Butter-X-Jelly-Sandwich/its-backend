from django.urls import include, path
from rest_framework import routers

from .views import StudentSubmissionViewSet, TutorSubmissionViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(
    r"student/submission",
    StudentSubmissionViewSet,
    basename="student-submission",
)

router.register(
    r"tutor/submission", TutorSubmissionViewSet, basename="tutor-submission"
)

urlpatterns = [
    path("", include(router.urls)),
]
