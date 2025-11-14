from rest_framework.response import Response
from rest_framework import status


def handle_permission_denied_review(self):
    """Called when a user tries to add a review but are business users."""
    message = 'Mit einem Geschäftsprofil dürfen keine Bewertungen abgegeben werden.'
    return Response({'error': message}, status=status.HTTP_403_FORBIDDEN)
