from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken

from auth_app.models import CustomUser

from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .handlers import get_registration_serializer, handle_registration_success, handle_invalid_credentials, handle_login_success
from .services import authenticate_user


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
        return handle_invalid_credentials(self, serializer)
    

class UserLoginView(ObtainAuthToken):
    """
    View for User Login.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        """
        POST-Handler for User Login. Handles the request with different responses based on authentication result.
        """
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return handle_invalid_credentials(self, serializer)
        user = authenticate_user(username=request.data.get('username'), password=request.data.get('password'))
        if user is not None:
            return handle_login_success(self, user)
        return handle_invalid_credentials(self, serializer)
    

class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating and deleting User Profile.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        print(CustomUser.objects.all())
        return CustomUser.objects.all()