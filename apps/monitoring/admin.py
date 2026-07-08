"""
Admin configuration for the Monitoring application.

This file tells Django Admin:

- Which models should appear in the Admin Panel.
- Which columns should be displayed.
- Which filters should be available.
- Which fields should be searchable.

Without registering a model here, it will not appear in
the Django Admin interface.
"""

# Import Django's admin module.
# This provides tools to customize the Django Admin Panel.
from django.contrib import admin

# Import the models we want to manage in the Admin Panel.
from .models import MonitoringJob, Server


# =====================================================================
# Server Admin Configuration
# =====================================================================

# Register the Server model with Django Admin.
# This decorator automatically registers the model and
# associates it with the ServerAdmin configuration below.
@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    """
    Custom Admin configuration for the Server model.

    Controls how Server objects appear inside Django Admin.
    """

    # ----------------------------------------------------------
    # Columns displayed in the server list page.
    #
    # Instead of displaying only:
    #
    # Local API
    #
    # Django will display:
    #
    # Name | Host | Port | Type | Status | Active
    # ----------------------------------------------------------
    list_display = (
        "name",
        "host",
        "port",
        "resource_type",
        "status",
        "is_active",
    )

    # ----------------------------------------------------------
    # Filters shown on the right side of Django Admin.
    #
    # Allows administrators to quickly filter servers.
    #
    # Example:
    # Show only:
    #   ✓ APIs
    #   ✓ Online servers
    #   ✓ Active servers
    # ----------------------------------------------------------
    list_filter = (
        "resource_type",
        "status",
        "is_active",
    )

    # ----------------------------------------------------------
    # Search box configuration.
    #
    # Users can search using:
    #
    # - Server Name
    # - Hostname
    #
    # Example:
    # "localhost"
    # "127.0.0.1"
    # "Production API"
    # ----------------------------------------------------------
    search_fields = (
        "name",
        "host",
    )


# =====================================================================
# Monitoring Job Admin Configuration
# =====================================================================

# Register the MonitoringJob model.
@admin.register(MonitoringJob)
class MonitoringJobAdmin(admin.ModelAdmin):
    """
    Admin configuration for Monitoring Jobs.
    """

    # ----------------------------------------------------------
    # Columns displayed in the Monitoring Job list.
    #
    # Example:
    #
    # API Health Check
    # Local Django API
    # API
    # Every 60 seconds
    # Enabled
    # ----------------------------------------------------------
    list_display = (
        "name",
        "server",
        "job_type",
        "interval_seconds",
        "enabled",
    )

    # ----------------------------------------------------------
    # Filters available in the Admin Panel.
    #
    # Allows filtering by:
    #
    # - Job Type
    # - Enabled / Disabled
    # ----------------------------------------------------------
    list_filter = (
        "job_type",
        "enabled",
    )

    # ----------------------------------------------------------
    # Search Monitoring Jobs.
    #
    # Search by:
    #
    # - Job Name
    # - Server Name
    #
    # Notice:
    #
    # server__name
    #
    # means:
    #
    # MonitoringJob
    #       ↓
    #     Server
    #       ↓
    #     name field
    # ----------------------------------------------------------
    search_fields = (
        "name",
        "server__name",
    )
