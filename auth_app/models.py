from django.db import models
from django.contrib.auth.models import User


"""
The `USER_TYPES` variable is a list of tuples in Python. Each tuple represents a choice for the type of the created user.
"""
USER_TYPES = [
    ('customer', 'Customer'),
    ('business', 'Business'),
]


class CustomUser(models.Model):
    """
    The `CustomUser` class extends the `User` model with fields for user information, including a file, location, telephone number, description, working hours, and type.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=USER_TYPES)
    file = models.FileField(upload_to='profiles/', blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')
    tel = models.CharField(max_length=20, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
