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
    user = serializers.IntegerField(source='id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = CustomUser
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']