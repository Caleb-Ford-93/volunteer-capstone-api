from django.db import models
from django.contrib.auth.models import User


class Volunteer(models.Model):
    phone_number = models.CharField(max_length=10)
    location = models.CharField(max_length=255)
    user = models.OneToOneField(
        User, related_name="volunteer", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
