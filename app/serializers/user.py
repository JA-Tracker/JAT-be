from rest_framework import serializers
from ..models import User

class UserSerializer(serializers.ModelSerializer):
    """User Display Serializer with explicit output structure"""

    def to_representation(self, instance):
        response = {}
        response["id"] = instance.id
        response["username"] = instance.username
        response["email"] = instance.email
        response["role"] = instance.role
        response["created_at"] = instance.created_at
        response["updated_at"] = instance.updated_at
        return response

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'created_at', 'updated_at')
        read_only_fields = fields

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
