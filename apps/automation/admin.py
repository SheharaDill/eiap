"""
Admin configuration for the Automation application.

This module configures how automation rules are displayed
inside the Django Admin Panel.

Administrators can:

- Create automation rules
- Enable or disable rules
- Change thresholds
- Select actions
- Assign priorities

without modifying application code.
"""

from django.contrib import admin

from .models import AutomationRule


# ==========================================================
# Automation Rule Admin
# ==========================================================

@admin.register(AutomationRule)
class AutomationRuleAdmin(admin.ModelAdmin):
    """
    Admin configuration for Automation Rules.
    """

    # ------------------------------------------------------
    # Columns displayed in the list page.
    # ------------------------------------------------------
    list_display = (
        "name",
        "server",
        "metric_type",
        "operator",
        "threshold",
        "action",
        "priority",
        "enabled",
    )

    # ------------------------------------------------------
    # Filters displayed on the right side.
    # ------------------------------------------------------
    list_filter = (
        "metric_type",
        "action",
        "enabled",
    )

    # ------------------------------------------------------
    # Search box configuration.
    # ------------------------------------------------------
    search_fields = (
        "name",
        "server__name",
    )

    # ------------------------------------------------------
    # Default ordering.
    # Highest priority rules appear first.
    # ------------------------------------------------------
    ordering = (
        "priority",
        "name",
    )
