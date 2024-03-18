from django.db import models

from ..questions.models import Question


# from django.contrib.postgres.fields import ArrayField
class Submissiondata(models.Model):
    LANGUAGE_CHOICES = [
        ("python", "python"),
        ("c", "c"),
    ]
    qn_id = models.IntegerField()
    language = models.CharField(max_length=20, blank=True, choices=LANGUAGE_CHOICES)
    submission_number = models.IntegerField()
    submission_date = models.DateTimeField(auto_now_add=True)
    program = models.CharField(max_length=10000)
    status = models.CharField(max_length=10000, blank=True, null=True)
    score = models.IntegerField()
    tutor_feedback = models.CharField(max_length=10000, blank=True, null=True)
    its_feedback_hint_student = models.JSONField(null=True)
    its_feedback_fix_tutor = models.JSONField(null=True)
    total_score = models.IntegerField()
    submitted_by = models.ForeignKey(
        "accounts.CustomUser", blank=True, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        qn_title = Question.objects.get(pk=self.qn_id).question_title
        return f"Question {self.qn_id}: {qn_title} | Submission ID: {str(self.pk)}"


# class ITSFeedback(models.Model):
#     submission = models.ForeignKey(Submissiondata, on_delete=models.CASCADE)
#     line = models.IntegerField(null = True)
#     feedback = models.CharField(max_length=10000)

#     def __str__(self):
#         return ', '.join(self.feedback) if self.feedback else "No feedback"
