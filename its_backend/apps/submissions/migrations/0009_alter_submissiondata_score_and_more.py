# Generated by Django 5.0.2 on 2024-04-02 16:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("submissions", "0008_alter_submissiondata_its_feedback_fix_tutor_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="submissiondata",
            name="score",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="submissiondata",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("pending", "pending"), ("completed", "completed")],
                max_length=10000,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="submissiondata",
            name="submission_number",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="submissiondata",
            name="total_score",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
