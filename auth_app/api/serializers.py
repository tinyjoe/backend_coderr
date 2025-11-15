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
        """
        Validate registration data using custom validator.
        """
        return validate_registration_data(attrs)

    def create(self, validated_data):
        """
        Create a new user using the service function.
        """
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
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    class Meta:
        model = CustomUser
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']

    def update(self, instance, validated_data):
        """
        Update user profile information.
        """
        user_data = validated_data.pop('user', {})
        for field, value in user_data.items():
            setattr(instance.user, field, value)
        instance.user.save()
        return super().update(instance, validated_data)


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing users.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type']