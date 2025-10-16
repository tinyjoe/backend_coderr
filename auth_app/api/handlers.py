from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRegistrationSerializer

def get_registration_serializer(self, request):
    """Initializes the serializer with request data."""
    return UserRegistrationSerializer(data=request.data)

def handle_registration_success(self, serializer):
    """Called when the serializer is valid."""
    data = serializer.save()
    message = "Der Benutzer wurde erfolgreich erstellt."
    return Response(data, status=status.HTTP_201_CREATED)

def handle_registration_invalid(self, serializer):
    """Called when the validation fails."""
    message = "Ungültige Anfragedaten."  # nur intern
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)