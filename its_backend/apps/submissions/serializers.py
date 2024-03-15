from rest_framework import serializers
from .models import Submissiondata, ITS_Feedback
from ..accounts.serializers import RetrieveUserSerializer

class RetrieveAllSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submissiondata
        fields = ['pk', 'submission_number', 'score', 'total_score', 'submission_date']

class CreateITSFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ITS_Feedback
        fields = ['pk','line', 'feedback']
        
class RetrieveSubmissionDetailsSerializer(serializers.ModelSerializer):
    its_feedback = CreateITSFeedbackSerializer(many=True, read_only=True, required=False)
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
        fields = ['pk',
                    'qn_id',
                    'submission_number',
                    'language',
                    'submission_date',
                    'program',
                    'its_feedback',
                    'report',
                    'total_score',
                    'score',
                    ]

    def to_representation(self, data):
        obj = super().to_representation(data)
        its_feedback = data.its_feedback_set.all()  # Access related ITS_Feedback instances through the reverse relation
        obj["its_feedback"] = CreateITSFeedbackSerializer(its_feedback, many=True, required=False).data
        return obj


class CreateSubmissionSerializer(serializers.ModelSerializer):
    its_feedback = CreateITSFeedbackSerializer(many=True, write_only=True, required=False)
    submitted_by = RetrieveUserSerializer(read_only=True)
    class Meta:
        model = Submissiondata
        fields = ['pk', 
            'qn_id',
            'submission_number',
            'language', 
            'submission_date', 
            'program',
            'its_feedback', 
            'report',
            'total_score',
            'score',
            'submitted_by'
        ]

    def create(self, validated_data):
        print("valiodated ", validated_data)
        its_feedback_data = validated_data.pop("its_feedback", None)

        submissiondata = Submissiondata.objects.create(
            **validated_data, submitted_by=self.context["user"]
        )
        print("its_feedback", its_feedback_data)
        if its_feedback_data:
            for feedback in its_feedback_data:
                ITS_Feedback.objects.create(Submissiondata=submissiondata, **feedback)
        
        return submissiondata
