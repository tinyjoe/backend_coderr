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
    message = 'Ungültige Anfragedaten.'
    return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

def handle_login_success(self, user):
    """Called when user authentication is successful."""
    token, _ = Token.objects.get_or_create(user=user)
    message = 'Erfolgreiche Anmeldung.'
    data = {'token': token.key, 'username': user.username, 'email': user.email, 'user_id': user.id}
    return Response(data, status=status.HTTP_200_OK)

def handle_unauthenticated_access(self):
    """Called when an unauthenticated user tries to access a protected resource."""
    message = 'Benutzer ist nicht authentifiziert.'
    return Response({'error': message}, status=status.HTTP_401_UNAUTHORIZED)

def handle_profile_not_found(self):
    """Called when the requested user profile does not exist."""
    message = 'Das Benutzerprofil wurde nicht gefunden.'
    return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)

def handle_profile_data_success(self, serializer):
    """Called when user profile data is successfully retrieved or updated."""
    message = 'Die Profildaten wurden erfolgreich abgerufen.'
    return Response(serializer.data, status=status.HTTP_200_OK)

def handle_profile_update_success(self, serializer):
    """Called when user profile data is successfully updated."""
    message = 'Das Profil wurde erfolgreich aktualisiert.'
    return Response(serializer.data, status=status.HTTP_200_OK)

def handle_forbidden_profile_access(self):
    """Called when a user tries to access or modify another user's profile."""
    message = 'Authentifizierter Benutzer ist nicht der Eigentümer des Profils'
    return Response({'error': message}, status=status.HTTP_403_FORBIDDEN)
