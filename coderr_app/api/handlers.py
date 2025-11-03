from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

def handle_unauthenticated_access(self):
    """Called when an unauthenticated user tries to access a protected resource."""
    message = 'Der Benutzer ist nicht authentifiziert.'
    return Response({'error': message}, status=status.HTTP_401_UNAUTHORIZED)


def handle_create_review_success(self, serializer):
    """Called when a review is successfully created."""
    message = 'Die Bewertung wurde erfolgreich erstellt.'
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def handle_create_review_failure(self):
    """Called when review creation fails."""
    message = 'Fehlerhafte Anfrage. Der Benutzer hat möglicherweise bereits eine Bewertung für das gleiche Geschäftsprofil abgegeben.'
    return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)


def handle_unauthenticated_review_access(self):
    """Called when an unauthenticated user tries to create a review."""
    message = 'Unauthorized. Der Benutzer muss authentifiziert sein und ein Kundenprofil besitzen.'
    return Response({'error': message}, status=status.HTTP_401_UNAUTHORIZED)


def handle_permission_denied_review(self):
    """Called when a user tries to add a review but are business users."""
    message = 'Mit einem Geschäftsprofil dürfen keine Bewertungen abgegeben werden.'
    return Response({'error': message}, status=status.HTTP_403_FORBIDDEN)


def handle_update_review_success(self, serializer):
    """Called when a review is successfully updated."""
    message = 'Die Bewertung wurde erfolgreich aktualisiert.'
    return Response(serializer.data, status=status.HTTP_200_OK)


def handle_update_review_failure(self):
    """Called when review update fails."""
    message = 'Fehlerhafte Anfrage. Die Bewertung konnte nicht aktualisiert werden.'
    return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)


def handle_update_review_permission_denied(self):
    """Called when a user tries to update a review they do not own."""
    message = 'Der Benutzer ist nicht berechtigt, diese Bewertung zu bearbeiten.'
    return Response({'error': message}, status=status.HTTP_403_FORBIDDEN)


def handle_review_not_found(self):
    """Called when a review is not found."""
    message = 'Es wurde keine Bewertung mit der angegebenen ID gefunden.'
    return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)


def handle_delete_review_success(self):
    """Called when a review is successfully deleted."""
    message = 'Die Bewertung wurde erfolgreich gelöscht.'
    return Response({'message': message}, status=status.HTTP_204_NO_CONTENT)


def handle_delete_review_permission_denied(self):
    """Called when a user tries to delete a review they do not own."""
    message = 'Der Benutzer ist nicht berechtigt, diese Bewertung zu löschen.'
    return Response({'error': message}, status=status.HTTP_403_FORBIDDEN)


def handle_create_order_success(self, serializer):
    """Called when an order is successfully created."""
    message = 'Die Bestellung wurde erfolgreich erstellt.'
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def handle_create_order_failure(self):
    """Called when order creation fails."""
    message = 'Fehlerhafte Anfrage. Die Bestellung konnte nicht erstellt werden.'
    return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

def handle_create_order_permission_denied(self):
    """Called when a user tries to create an order but are business users."""
    message = 'Mit einem Geschäftsprofil dürfen keine Bestellungen aufgegeben werden.'
    return Response({'error': message}, status=status.HTTP_403_FORBIDDEN)

def handle_offer_detail_not_found(self):
    """Called when an offer detail is not found."""
    message = 'Es wurde kein Angebotsdetail mit der angegebenen ID gefunden.'
    return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)