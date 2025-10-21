from django.contrib import admin
from django.urls import path

from .views import UserRegistrationView, UserLoginView, UserProfileDetailView, BusinessUserListView, CustomerUserListView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('profiles/business/', BusinessUserListView.as_view(), name='business-user-list'),
    path('profiles/customer/', CustomerUserListView.as_view(), name='customer-user-list'),
]