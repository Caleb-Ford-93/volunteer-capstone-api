from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    location = models.CharField(max_length=100)
    user = models.OneToOneField(
        User, related_name="organization", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
