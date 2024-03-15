from django.db import models

# from django.contrib.postgres.fields import ArrayField

class Submissiondata(models.Model):
    qn_id = models.IntegerField()
    language = models.CharField(max_length=30, default = 'py')
    submission_number = models.IntegerField()
    submission_date = models.DateTimeField(auto_now_add=True)
    program = models.CharField(max_length=10000)
    tutor_feedback = models.CharField(max_length=10000, blank=True, null=True)  
    report = models.CharField(max_length=10000, blank=True, null=True)
    score = models.IntegerField()
    total_score = models.IntegerField()
    submitted_by = models.ForeignKey(
        "accounts.CustomUser", blank=True, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return super().__str__()
    
class ITSFeedback(models.Model):
    submission = models.ForeignKey(Submissiondata, on_delete=models.CASCADE)
    line = models.IntegerField(null = True)
    feedback = models.CharField(max_length=10000)

    def __str__(self):
        return ', '.join(self.feedback) if self.feedback else "No feedback"
    