from rest_framework import serializers
from ..models import Application

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
        response["notes"] = instance.notes
        response["jobUrl"] = instance.job_url
        response["contactPerson"] = instance.contact_person
        response["contactEmail"] = instance.contact_email
        response["createdAt"] = instance.created_at
        response["updatedAt"] = instance.updated_at
        return response

    class Meta:
        model = Application
        fields = (
            'id', 'company', 'position', 'applied_date', 'status', 'interview_date',
            'follow_up_date', 'salary', 'job_type', 'notes', 'job_url',
            'contact_person', 'contact_email', 'created_at', 'updated_at'
        )
        read_only_fields = fields

class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Application Create Serializer for creating new applications"""

    class Meta:
        model = Application
        fields = (
            'company', 'position', 'applied_date', 'status', 'interview_date',
            'follow_up_date', 'salary', 'job_type', 'notes', 'job_url',
            'contact_person', 'contact_email'
        )

    def create(self, validated_data):
        # Set the user from the request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ApplicationUpdateSerializer(serializers.ModelSerializer):
    """Application Update Serializer for updating existing applications"""

    class Meta:
        model = Application
        fields = (
            'company', 'position', 'applied_date', 'status', 'interview_date',
            'follow_up_date', 'salary', 'job_type', 'notes', 'job_url',
            'contact_person', 'contact_email'
        ) 