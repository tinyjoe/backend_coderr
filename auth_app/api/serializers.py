from rest_framework import serializers

from auth_app.models import CustomUser
from .validators import validate_registration_data
from .services import create_user


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for User Registration. 
    """
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        return validate_registration_data(attrs)

    def create(self, validated_data):
        return create_user(validated_data)
    

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for User Login.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for User Profile.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'type']