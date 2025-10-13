from django.db import models
from django.contrib.auth.models import User

USER_TYPES = [
    ('customer', 'Customer'),
    ('business', 'Business'),
]

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=USER_TYPES)


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='profiles/', null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    working_hours = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=10, choices=USER_TYPES, null=True, blank=True)
