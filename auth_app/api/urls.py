from django.contrib import admin
from django.urls import path

from .views import UserRegistrationView, UserLoginView, UserProfileDetailView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='user-profile-detail'),
]