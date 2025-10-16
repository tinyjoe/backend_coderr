from django.contrib import admin
from django.urls import path

from .views import UserRegistrationView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='user-registration'),
]