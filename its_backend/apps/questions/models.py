from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone

def get_default_due_date():
    return timezone.now() + relativedelta(days=30)


class Question(models.Model):
    LANGUAGE_CHOICES = [
        ("PY", "Python"),
        ("JAVA", "Java"),
        ("JS", "JavaScript"),
        ("CPP", "C++"),
    ]

    question_title = models.CharField(max_length=200, blank=False)
    question_statement = models.TextField(blank=False)
    ref_program = models.TextField(blank=True)
    language = models.CharField(max_length=20, blank=True, choices=LANGUAGE_CHOICES)
    pub_date = models.DateTimeField(blank=True, auto_now=True)
    pub_by = models.ForeignKey(
        "accounts.CustomUser", blank=True, on_delete=models.CASCADE
    )
    due_date = models.DateField(blank=True, default=get_default_due_date)

    def __str__(self):
        return self.question_title


class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    input = models.TextField(blank=False)
    output = models.TextField(blank=False)

    def __str__(self):
        return f"{self.question.question_title} Test Case"
