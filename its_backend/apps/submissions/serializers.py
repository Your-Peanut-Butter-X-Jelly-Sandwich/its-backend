from rest_framework import serializers

from .models import Submissiondata


class RetrieveSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submissiondata
        fields = ['id', 'qn_id', 'language', 'submisson_date', 'program', 'feedback', 'report']


class CreateSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submissiondata
        fields = ['id', 'language', 'submisson_date', 'program']

class CreateFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submissiondata
        fields = ['feedback']
