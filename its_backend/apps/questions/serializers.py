from rest_framework import serializers
from .models import Question, TestCase
from ..accounts.serializers import RetrieveUserSerializer


class StudentQuestionListSerializer(serializers.ModelSerializer):
    question_title = serializers.CharField(read_only=True)
    pub_by = RetrieveUserSerializer(read_only=True)
    pub_date = serializers.DateTimeField(read_only=True)
    due_date = serializers.DateField(read_only=True)

    class Meta:
        model = Question
        fields = ["pk", "question_title", "pub_date", "due_date", "pub_by"]


class StudentQuestionDetailSerializer(serializers.ModelSerializer):
    pub_by = RetrieveUserSerializer(read_only=True)
    pub_date = serializers.DateTimeField(read_only=True)
    due_date = serializers.DateField(read_only=True)
    language = serializers.CharField(read_only=True)
    question_statement = serializers.CharField(read_only=True)
    question_title = serializers.CharField(read_only=True)
    pk = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = [
            "pub_by",
            "pub_date",
            "due_date",
            "language",
            "question_statement",
            "question_title",
            "pk",
        ]


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ["pk", "input", "output"]


class TutorCreateUpdateQuestionSerializer(serializers.ModelSerializer):
    test_cases = TestCaseSerializer(many=True, write_only=True)
    pub_by = RetrieveUserSerializer(read_only=True)
    pub_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Question
        fields = [
            "pk",
            "question_title",
            "question_statement",
            "ref_program",
            "language",
            "pub_date",
            "due_date",
            "pub_by",
            "test_cases",
        ]

    def create(self, validated_data):
        test_cases_data = validated_data.pop("test_cases", None)
        question = Question.objects.create(
            **validated_data, pub_by=self.context["user"]
        )
        for test_case_data in test_cases_data:
            TestCase.objects.create(question=question, **test_case_data)

        return question

    def update(self, instance, validated_data):
        test_cases_data = validated_data.pop("test_cases", None)
        fields = [
            "question_title",
            "question_statement",
            "ref_program",
            "due_date",
            "language",
        ]
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError as e:
                print(e)
                pass
        instance.save()
        if test_cases_data is not None:
            TestCase.objects.filter(question=instance).delete()
            for test_case_data in test_cases_data:
                TestCase.objects.create(question=instance, **test_case_data)
        return instance

    def to_representation(self, data):
        obj = super().to_representation(data)
        obj["test_cases"] = TestCaseSerializer(data.testcase_set, many=True).data
        return obj


class TutorQuestionDetailSerializer(serializers.ModelSerializer):
    test_cases = TestCaseSerializer(many=True, read_only=True, source="testcase_set")

    class Meta:
        model = Question
        exclude = ["pub_by"]

    def to_representation(self, data):
        obj = super().to_representation(data)
        obj["test_cases"] = TestCaseSerializer(data.testcase_set, many=True).data
        return obj


class TutorQuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["pk", "question_title", "pub_date", "due_date"]
