<<<<<<< HEAD
from django.urls import path, include
from .views import StudentSubmissionViewSet
from rest_framework import routers
=======
from django.urls import path
from .views import SubmissionHistoryView, CreateSubmissionView
>>>>>>> 28b5f5cac722d1f7eb2d81c8ac0c345feb680e69

# urlpatterns = [
#     path('student/question/<int:qn_id>/', CreateSubmissionView.as_view(), name='create_submission'),
#     path('student/question/<int:qn_id>/past_submissions/', SubmissionHistoryView.as_view(actions={'get': 'list'}), name='submission_history'),
# ]
router = routers.SimpleRouter(trailing_slash=False)
router.register(
    r"student/submission", StudentSubmissionViewSet, basename="student-submission"
)

urlpatterns = [
    path("", include(router.urls)),
]