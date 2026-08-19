"""Database models for the profiles application."""

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Represent a user profile."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """Return the username associated with the profile."""
        return self.user.username
