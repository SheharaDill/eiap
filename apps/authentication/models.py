"""
Authentication models for EIAP.

This module defines the custom User model used throughout the platform.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    """
    Available roles within the platform.
    """

    ADMIN = "ADMIN", "Administrator"
    OPERATOR = "OPERATOR", "Operator"
    VIEWER = "VIEWER", "Viewer"


class User(AbstractUser):
    """
    Custom user model for EIAP.

    Extends Django's AbstractUser by adding fields that are useful
    for infrastructure operations and role-based access control.
    """

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.VIEWER,
    )

    department = models.CharField(
        max_length=100,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.username
