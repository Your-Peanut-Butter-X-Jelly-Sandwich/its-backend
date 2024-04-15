from django.db import models

from ..questions.models import Question


class Submissiondata(models.Model):
    LANGUAGE_CHOICES = [
        ("python", "python"),
        ("c", "c"),
    ]
    qn_id = models.IntegerField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    submission_number = models.IntegerField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    program = models.CharField(max_length=10000)
    status = models.CharField(max_length=10000, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    tutor_feedback = models.CharField(max_length=10000, blank=True, null=True)
    its_feedback_hint_student = models.JSONField(blank=True, null=True)
    its_feedback_fix_tutor = models.JSONField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    submitted_by = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)

    def __str__(self) -> str:
        qn_title = Question.objects.get(pk=self.qn_id).question_title
        return f"Question {self.qn_id}: {qn_title} | Submission ID: {str(self.pk)} | By: {str(self.submitted_by.pk)}"
