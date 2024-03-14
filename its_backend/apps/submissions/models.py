from django.db import models
# from its_backend.apps.accounts.models import CustomUser

class Submissiondata(models.Model):
    # foreign key to students and problem
    # problem = models.ForeignKey
    # student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    qn_id = models.IntegerField()
    language = models.CharField(max_length=30, default = 'py')
    submisson_date = models.DateTimeField(auto_now_add=True)
    program = models.CharField(max_length=10000)
    # The blank=True parameter allows these fields to be optional when validating forms.
    # The null=True parameter allows these fields to have a NULL value in the database.
    feedback = models.CharField(max_length=10000, blank=True, null=True)   
    report = models.CharField(max_length=10000, blank=True, null=True)
    
    def __str__(self) -> str:
        return super().__str__()
    