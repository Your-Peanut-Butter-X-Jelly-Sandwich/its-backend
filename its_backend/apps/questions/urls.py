from django.urls import include, path
from rest_framework_nested import routers

from .views import (
    StudentDashboardStatisticsView,
    StudentQuestionViewSet,
    TutorDashboardStatisticsView,
    TutorQuestionViewSet,
)

router = routers.SimpleRouter(trailing_slash=False)
router.register(
    r"student/question", StudentQuestionViewSet, basename="student-questions"
)
router.register(r"tutor/question", TutorQuestionViewSet, basename="tutor-questions")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "student/dashboard-stats",
        StudentDashboardStatisticsView.as_view(),
        name="student-dashboard-stats",
    ),
    path(
        "tutor/dashboard-stats",
        TutorDashboardStatisticsView.as_view(),
        name="tutor-dashboard-stats",
    ),
]
