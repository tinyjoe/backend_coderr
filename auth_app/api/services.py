from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from ..models import CustomUser

def create_user(validated_data):
    """
    Creates a User, Custom User and a Token.
    """
    validated_data.pop('repeated_password')
    username = validated_data.pop('username')
    email = validated_data.pop('email')
    password = validated_data.pop('password')
    user = User.objects.create_user(username=username, email=email, password=password)
    CustomUser.objects.create(user=user, type=validated_data['type'])
    token, _ = Token.objects.get_or_create(user=user)
    return {'token': token.key, 'username': user.username, 'email': user.email, 'user_id': user.id}