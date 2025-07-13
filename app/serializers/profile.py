from rest_framework import serializers
from ..models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """Profile Display Serializer with explicit output structure"""

    def to_representation(self, instance):
        response = {}
        response["id"] = instance.id
        response["username"] = instance.user.username if instance.user else None
        response["email"] = instance.user.email if instance.user else None
        response["first_name"] = instance.first_name
        response["middle_name"] = instance.middle_name
        response["last_name"] = instance.last_name
        response["birth_date"] = instance.birth_date
        
        return response 
    
    class Meta:
        model = Profile
        fields = ('first_name', 'middle_name', 'last_name', 'birth_date')