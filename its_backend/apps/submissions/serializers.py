from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from its_backend.apps.accounts.models import Teaches
from its_backend.apps.questions.models import Question

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
            "status",
            "total_score",
            "score",
        ]


class StudentRetrieveSubmissionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submissiondata
        exclude = ["its_feedback_fix_tutor"]


def check_is_question_accessible(student_id, question):
    # check if student has access to the question
    tutors = Teaches.objects.filter(student_id=student_id).values_list(
        "tutor_id", flat=True
    )
    question_pub_by = question.pub_by.pk
    result = question_pub_by in tutors
    return result


class QuestionNotAvailableToStudentError(Exception):
    pass


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
            "status",
            "total_score",
            "score",
            "submitted_by",
        ]

    def create(self, validated_data):
        user = self.context["user"]
        qn_id = validated_data["qn_id"]
        try:
            question = Question.objects.get(pk=qn_id)
        except Question.DoesNotExist:
            raise ObjectDoesNotExist(f"Question with qn_id {qn_id} not found") from None

        # check if student can submit to question
        if not check_is_question_accessible(user.pk, question):
            raise QuestionNotAvailableToStudentError(
                f"Question with qn_id {qn_id} is not available to the student"
            ) from None
        return Submissiondata.objects.create(
            **validated_data,
            submitted_by=user,
            status=self.context["status"],
        )

    def update(self, instance, validated_data):
        fields = [
            "qn_id",
            "submission_number",
            "its_feedback_hint_student",
            "its_feedback_fix_tutor",
            "tutor_feedback",
            "status",
            "total_score",
            "score",
        ]
        for field in fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()
        return instance
