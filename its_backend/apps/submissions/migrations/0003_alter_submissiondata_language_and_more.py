# Generated by Django 5.0.2 on 2024-03-16 06:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("submissions", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="submissiondata",
            name="language",
            field=models.CharField(
                blank=True, choices=[("PY", "python"), ("C", "c")], max_length=20
            ),
        ),
        migrations.AlterField(
            model_name="submissiondata",
            name="submitted_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
