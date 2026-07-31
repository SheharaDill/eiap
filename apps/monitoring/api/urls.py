"""
Monitoring API URLs

This module defines the REST API routes for the
Monitoring application.

Instead of manually creating every CRUD URL,
we use Django REST Framework's DefaultRouter.

The router automatically generates RESTful URLs
for every registered ViewSet.
"""

# Django REST Framework router.
from rest_framework.routers import DefaultRouter

# Monitoring API ViewSets.
from apps.monitoring.api.views import (
    ServerViewSet,
)

# ==========================================================
# Router
# ==========================================================

#
# Create the API router.
#
router = DefaultRouter()

#
# Register the Server API.
#
router.register(

    r"servers",

    ServerViewSet,

    basename="server",

)

#
# Export all generated URLs.
#
urlpatterns = router.urls
