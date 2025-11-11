from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken

from auth_app.models import CustomUser

from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserListSerializer
from .handlers import get_registration_serializer, handle_registration_success, handle_invalid_credentials, handle_login_success, handle_unauthenticated_access, handle_profile_not_found, handle_profile_data_success, handle_profile_update_success, handle_forbidden_profile_access
from .services import authenticate_user
from .permissions import IsAuthenticatedOrOwnProfile


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
    permission_classes = [IsAuthenticatedOrOwnProfile]
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        """
        GET-Handler for retrieving User Profile with different event handlers.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return handle_profile_data_success(self, serializer)
        except NotAuthenticated:
            return handle_unauthenticated_access(self)
        except PermissionDenied:
            return handle_forbidden_profile_access(self)
        except CustomUser.DoesNotExist:
            return handle_profile_not_found(self)
        
    def patch(self, request, *args, **kwargs):
        """
        PATCH-Handler for updating User Profile with different event handlers.
        """
        try: 
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return handle_profile_update_success(self, serializer)
        except NotAuthenticated:
            return handle_unauthenticated_access(self)
        except PermissionDenied:
            return handle_forbidden_profile_access(self)
        except CustomUser.DoesNotExist:
            return handle_profile_not_found(self)


class BusinessUserListView(generics.ListAPIView):
    """
    View for listing all Business Users.
    """
    queryset = CustomUser.objects.filter(type='business')
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer


class CustomerUserListView(generics.ListAPIView):
    """
    View for listing all Customer Users.
    """
    queryset = CustomUser.objects.filter(type='customer')
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer