from django.db import models
<<<<<<< HEAD
from django.contrib.postgres.fields import ArrayField

class Submissiondata(models.Model):
    def __str__(self) -> str:
        return super().__str__()
    
=======
# from its_backend.apps.accounts.models import CustomUser

class Submissiondata(models.Model):
    # foreign key to students and problem
    # problem = models.ForeignKey
    # student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

>>>>>>> 28b5f5cac722d1f7eb2d81c8ac0c345feb680e69
    qn_id = models.IntegerField()
    language = models.CharField(max_length=30, default = 'py')
    submission_number = models.IntegerField()
    submission_date = models.DateTimeField(auto_now_add=True)
    program = models.CharField(max_length=10000)
<<<<<<< HEAD
    tutor_feedback = models.CharField(max_length=10000, blank=True, null=True)  
    report = models.CharField(max_length=10000, blank=True, null=True)
    score = models.IntegerField()
    total_score = models.IntegerField()
    submitted_by = models.ForeignKey(
        "accounts.CustomUser", blank=True, on_delete=models.CASCADE
    )
    
class ITS_Feedback(models.Model):
    submission = models.ForeignKey(Submissiondata, on_delete=models.CASCADE)
    line = models.IntegerField(null = True)
    feedback = models.CharField(max_length=10000)

    def __str__(self):
        return ', '.join(self.feedback) if self.feedback else "No feedback"
=======
    # The blank=True parameter allows these fields to be optional when validating forms.
    # The null=True parameter allows these fields to have a NULL value in the database.
    feedback = models.CharField(max_length=10000, blank=True, null=True)   
    report = models.CharField(max_length=10000, blank=True, null=True)
    
    def __str__(self) -> str:
        return super().__str__()
>>>>>>> 28b5f5cac722d1f7eb2d81c8ac0c345feb680e69
    