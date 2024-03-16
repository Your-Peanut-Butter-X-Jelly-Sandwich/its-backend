from rest_framework import serializers

from ..accounts.serializers import RetrieveUserSerializer
from .models import Submissiondata


class RetrieveAllSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submissiondata
        fields = ["pk", "submission_number", "score", "total_score", "submission_date"]

class RetrieveSubmissionDetailsSerializer(serializers.ModelSerializer):
    # its_feedback = CreateITSFeedbackSerializer(many=True, read_only=True, required=False)
    qn_id = serializers.IntegerField(read_only=True)
    submission_number = serializers.IntegerField(read_only=True)
    language = serializers.CharField(read_only=True)
    submission_date = serializers.DateTimeField(read_only=True)
    program = serializers.CharField(read_only=True)
    report = serializers.CharField(read_only=True)
    total_score = serializers.IntegerField(read_only=True)
    score = serializers.IntegerField(read_only=True)

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
        ]

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
        submissiondata = Submissiondata.objects.create(
            **validated_data, submitted_by=self.context["user"]
        )
        return submissiondata
    
    def update(self, instance, validated_data):
        print("serializer update")
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