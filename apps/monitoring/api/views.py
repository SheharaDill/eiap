"""
Monitoring API Views

This module contains REST API endpoints for the
Monitoring application.

The API layer sits between:

Client
   │
   ▼
REST API
   │
   ▼
Django Models

Each ViewSet exposes CRUD operations for a model.
"""

# Django REST Framework ViewSets.
from rest_framework import viewsets

# Monitoring models.
from apps.monitoring.models import Server

# API serializers.
from apps.monitoring.api.serializers import (
    ServerSerializer,
)


class ServerViewSet(viewsets.ModelViewSet):
    """
    REST API for the Server model.

    ModelViewSet automatically provides:

    • List servers
    • Retrieve server
    • Create server
    • Update server
    • Delete server

    No additional CRUD methods are required unless
    custom behavior is needed.
    """

    #
    # Database records available through this API.
    #
    queryset = Server.objects.all()

    #
    # Serializer used to convert between
    # Django models and JSON.
    #
    serializer_class = ServerSerializer
