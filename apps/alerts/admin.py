"""
Admin configuration for the Alerts application.

This file tells Django Admin how Alert records should
appear inside the Admin interface.
"""

# Django Admin module.
from django.contrib import admin

# Import Alert model.
from .models import Alert


# ==========================================================
# Alert Admin
# ==========================================================

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    """
    Admin configuration for Alert records.
    """

    # ------------------------------------------------------
    # Columns displayed in the alert list.
    # ------------------------------------------------------
    list_display = (
        "id",
        "server",
        "name",
        "severity",
        "status",
        "created_at",
        "resolved_at",
    )

    # ------------------------------------------------------
    # Filters shown in the right sidebar.
    # ------------------------------------------------------
    list_filter = (
        "severity",
        "status",
        "server",
    )

    # ------------------------------------------------------
    # Search bar.
    # ------------------------------------------------------
    search_fields = (
        "name",
        "message",
        "server__name",
    )

    # ------------------------------------------------------
    # Show newest alerts first.
    # ------------------------------------------------------
    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "resolved_at",
        "acknowledged_at",
    )
