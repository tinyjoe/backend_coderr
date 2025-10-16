from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRegistrationSerializer
from .handlers import get_registration_serializer, handle_registration_success, handle_registration_invalid


class UserRegistrationView(APIView):
    """
    View for Registration of new User.
    """
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        """
        POST-Handler for User Registration. Handles the request by using helper functions from handlers.py.
        """
        serializer = get_registration_serializer(self, request)
        if serializer.is_valid():
            return handle_registration_success(self, serializer)
        return handle_registration_invalid(self, serializer)