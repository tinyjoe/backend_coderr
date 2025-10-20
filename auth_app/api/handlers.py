
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import UserRegistrationSerializer

def get_registration_serializer(self, request):
    """Initializes the serializer with request data."""
    return UserRegistrationSerializer(data=request.data)

def handle_registration_success(self, serializer):
    """Called when the serializer is valid."""
    data = serializer.save()
    message = 'Der Benutzer wurde erfolgreich erstellt.'
    return Response(data, status=status.HTTP_201_CREATED)

def handle_invalid_credentials(self, serializer):
    """Called when the validation fails."""
    message = 'Ungültige Anfragedaten.'  # nur intern
    return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

def handle_login_success(self, user):
    """Called when user authentication is successful."""
    token, _ = Token.objects.get_or_create(user=user)
    data = {'token': token.key, 'username': user.username, 'email': user.email, 'user_id': user.id}
    return Response(data, status=status.HTTP_200_OK)