from rest_framework import serializers

def validate_registration_data(attrs):
    """
    Validates the passwords for User Registration.
    """
    if attrs.get('password') != attrs.get('repeated_password'):
        raise serializers.ValidationError({"error": "Passwords do not match."})
    return attrs