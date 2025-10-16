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
The `CustomUser` class extends the `User` model with an additional `type` field.
"""
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=USER_TYPES)


""" The `UserProfile` class defines a model with fields for user information, including a file, location, telephone number, description, working hours, and type.
"""
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    file = models.FileField(upload_to='profiles/', null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    working_hours = models.CharField(max_length=100, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, null=True, blank=True)
