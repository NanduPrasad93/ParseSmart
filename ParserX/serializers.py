from rest_framework import serializers
from .models import InterviewResponse

class InterviewResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewResponse
        fields = ['id', 'question', 'answer', 'score', 'feedback', 'created_at']
