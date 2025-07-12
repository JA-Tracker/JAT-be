from rest_framework import serializers
from ..models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """Profile Display Serializer with explicit output structure"""

    def to_representation(self, instance):
        response = {}
        response["id"] = instance.id
        response["username"] = instance.user.username if instance.user else None
        response["email"] = instance.user.email if instance.user else None
        response["bio"] = instance.bio
        response["location"] = instance.location
        response["birth_date"] = instance.birth_date
        response["avatar"] = instance.avatar.url if instance.avatar else None
        response["created_at"] = instance.created_at
        response["updated_at"] = instance.updated_at
        return response

    class Meta:
        model = Profile
        fields = ('id', 'username', 'email', 'bio', 'location', 'birth_date', 'avatar', 'created_at', 'updated_at')
        read_only_fields = fields 