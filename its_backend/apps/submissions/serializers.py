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


# class CreateITSFeedbackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ITSFeedback
#         fields = ['pk','line', 'feedback']


class TutorRetrieveSubmissionDetailsSerializer(serializers.ModelSerializer):
    # its_feedback = CreateITSFeedbackSerializer(many=True, read_only=True, required=False)
    # qn_id = serializers.IntegerField(read_only=True)
    # submission_number = serializers.IntegerField(read_only=True)
    # language = serializers.CharField(read_only=True)
    # submission_date = serializers.DateTimeField(read_only=True)
    # program = serializers.CharField(read_only=True)
    # report = serializers.CharField(read_only=True)
    # total_score = serializers.IntegerField(read_only=True)
    # score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Submissiondata
        fields = [
            "pk",
            "qn_id",
            "submission_number",
            "language",
            "submission_date",
            "program",
            # "its_feedback_hint_student",
            "its_feedback_fix_tutor",
            "tutor_feedback",
            "report",
            "total_score",
            "score",
        ]

    # def to_representation(self, data):
    #     obj = super().to_representation(data)
    #     # its_feedback = data.its_feedback_set.all()  # Access related ITS_Feedback instances through the reverse relation
    #     its_feedback = data.its_feedback_set.all()  # Access related ITS_Feedback instances through the reverse relation

    #     obj["its_feedback"] = CreateITSFeedbackSerializer(its_feedback, many=True, required=False).data
    #     return obj


class StudentRetrieveSubmissionDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submissiondata
        exclude = ["its_feedback_fix_tutor"]


class CreateSubmissionSerializer(serializers.ModelSerializer):
    # its_feedback = CreateITSFeedbackSerializer(many=True, write_only=True, required=False)
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
