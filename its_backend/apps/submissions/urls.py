from django.urls import path

from .views import CreateSubmissionView, SubmissionHistoryView

urlpatterns = [
    path('student/question/<int:qn_id>/', CreateSubmissionView.as_view(), name='create_submission'),
    path('student/question/<int:qn_id>/past_submissions/', SubmissionHistoryView.as_view(actions={'get': 'list'}), name='submission_history'),
]
