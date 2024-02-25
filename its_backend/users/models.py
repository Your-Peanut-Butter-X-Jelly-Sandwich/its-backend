from django.db import models
from django.contrib.auth.models import AbstractUser

# this the student Model
# Should rename to Sudent.
class CustomUser(AbstractUser):
    school = models.CharField(max_length=100, blank=True)