from rest_framework import serializers

from ..accounts.serializers import RetrieveUserSerializer
from .models import Submissiondata


class RetrieveAllSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submissiondata
        fields = [
            "pk",
            "submission_number",
            "submitted_by",
            "score",
            "total_score",
            "submission_date",
        ]

    def to_representation(self, data):
        obj = super().to_representation(data)
        obj["submitted_by"] = RetrieveUserSerializer(data.submitted_by).data
        return obj


class TutorRetrieveSubmissionDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submissiondata
        fields = [
            "pk",
            "qn_id",
            "submission_number",
            "language",
            "submission_date",
            "program",
            "its_feedback_fix_tutor",
            "tutor_feedback",
            "report",
            "total_score",
            "score",
        ]


class StudentRetrieveSubmissionDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submissiondata
        exclude = ["its_feedback_fix_tutor"]


class CreateUpdateSubmissionSerializer(serializers.ModelSerializer):
    submitted_by = RetrieveUserSerializer(read_only=True)

    class Meta:
        model = Submissiondata
        fields = [
            "pk",
            "qn_id",
            "submission_number",
            "language",
            "submission_date",
            "program",
            "its_feedback_hint_student",
            "its_feedback_fix_tutor",
            "tutor_feedback",
            "report",
            "total_score",
            "score",
            "submitted_by",
        ]

    def create(self, validated_data):
        return Submissiondata.objects.create(
            **validated_data, submitted_by=self.context["user"]
        )

    def update(self, instance, validated_data):
        fields = [
            "tutor_feedback",
        ]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError as e:
                print(e)
                pass
        instance.save()
        return instance
