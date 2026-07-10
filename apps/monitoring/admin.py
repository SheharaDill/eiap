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
from django.contrib import admin

# Import all monitoring models used by Django Admin.
from .models import (
    Server,
    MonitoringJob,
    Metric,
    HealthCheck,
)


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

# ==========================================================
# Metric Admin
# ==========================================================
#
# Configures how collected monitoring metrics appear in
# Django Admin.
#
# This allows administrators and developers to inspect
# collected infrastructure metrics without writing SQL.
#
# ==========================================================


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    """
    Admin configuration for Metric records.
    """

    # Columns displayed in the admin list page.
    list_display = (
        "server",
        "cpu_usage",
        "memory_usage",
        "disk_usage",
        "response_time",
        "status",
        "collected_at",
    )

    # Filters shown in the right sidebar.
    list_filter = (
        "status",
        "server",
    )

    # Search fields.
    search_fields = (
        "server__name",
    )

    # Default ordering.
    ordering = (
        "-collected_at",
    )

# ==========================================================
# Health Check Admin
# ==========================================================
#
# Displays the execution history of every monitoring job.
#
# Unlike Metric records, HealthCheck records describe
# how the monitoring process itself performed.
#
# Example:
#
# Local Django API
# SUCCESS
# 125 ms
# 2026-07-09 10:30
#
# ==========================================================


@admin.register(HealthCheck)
class HealthCheckAdmin(admin.ModelAdmin):
    """
    Admin configuration for HealthCheck records.
    """

    # ------------------------------------------------------
    # Columns displayed in Django Admin.
    #
    # This lets administrators quickly see:
    #
    # • Which server was checked
    # • Which monitoring job executed
    # • Whether it succeeded
    # • How long it took
    # • When it started
    # ------------------------------------------------------
    list_display = (
        "server",
        "monitoring_job",
        "status",
        "execution_time_ms",
        "started_at",
    )

    # ------------------------------------------------------
    # Filters shown in the right sidebar.
    # ------------------------------------------------------
    list_filter = (
        "status",
    )

    # ------------------------------------------------------
    # Search by server name or monitoring job name.
    # ------------------------------------------------------
    search_fields = (
        "server__name",
        "monitoring_job__name",
    )

    # ------------------------------------------------------
    # Show newest executions first.
    # ------------------------------------------------------
    ordering = (
        "-started_at",
    )
