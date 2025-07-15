from rest_framework import serializers
from ..models import Application
from collections import Counter, defaultdict
from django.db.models import Avg

class ApplicationSerializer(serializers.ModelSerializer):
    """Application Display Serializer with explicit output structure"""

    def to_representation(self, instance):
        response = {}
        response["id"] = instance.id
        response["company"] = instance.company
        response["position"] = instance.position
        response["appliedDate"] = instance.applied_date.strftime('%Y-%m-%d') if instance.applied_date else None
        response["status"] = instance.status
        response["interviewDate"] = instance.interview_date.strftime('%Y-%m-%d') if instance.interview_date else None
        response["followUpDate"] = instance.follow_up_date.strftime('%Y-%m-%d') if instance.follow_up_date else None
        response["salary"] = instance.salary
        response["jobType"] = instance.job_type

        return response

class ApplicationCreateUpdateSerializer(serializers.ModelSerializer):
    """Application Write Serializer for creating and updating applications"""

    class Meta:
        model = Application
        fields = (
            'company', 'position', 'applied_date', 'status', 'interview_date',
            'follow_up_date', 'salary', 'job_type'
        )

    def create(self, validated_data):
        # Set the user from the request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data) 

class ApplicationStatsSerializer(serializers.Serializer):
    total_applications = serializers.IntegerField()
    interviews_scheduled = serializers.IntegerField()
    accepted_applications = serializers.IntegerField()
    rejected_applications = serializers.IntegerField()
    upcoming_interviews = serializers.ListField(child=serializers.DictField()) 

class CountPercentSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    percent = serializers.FloatField()

class ApplicationAnalyticsSerializer(serializers.Serializer):
    status_counts = serializers.DictField(child=CountPercentSerializer())
    job_type_counts = serializers.DictField(child=CountPercentSerializer())
    avg_salary_by_job_type = serializers.DictField(child=serializers.FloatField()) 
        