from django.db import models
from django.contrib.auth.models import User



"""
The `USER_TYPES` variable is a list of tuples in Python. Each tuple represents a choice for the type of the created user.
"""
USER_TYPES = [
    ('customer', 'Customer'),
    ('business', 'Business'),
]


"""
The `CustomUser` class extends the `User` model with fields for user information, including a file, location, telephone number, description, working hours, and type.
"""
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=USER_TYPES)
    file = models.FileField(upload_to='profiles/', null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    working_hours = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
