"""
Monitoring models for EIAP.

These models represent monitored infrastructure resources.
"""

from django.db import models


class ResourceType(models.TextChoices):
    """
    Types of monitored resources.
    """

    SERVER = "SERVER", "Server"
    WEBSITE = "WEBSITE", "Website"
    API = "API", "API"
    DATABASE = "DATABASE", "Database"


class ResourceStatus(models.TextChoices):
    """
    Current status of a monitored resource.
    """

    ONLINE = "ONLINE", "Online"
    OFFLINE = "OFFLINE", "Offline"
    UNKNOWN = "UNKNOWN", "Unknown"


class Server(models.Model):
    """
    Represents a monitored infrastructure resource.
    """

    name = models.CharField(max_length=100)

    host = models.CharField(
        max_length=255,
        help_text="Hostname or IP address",
    )

    port = models.PositiveIntegerField(default=80)

    resource_type = models.CharField(
        max_length=20,
        choices=ResourceType.choices,
        default=ResourceType.SERVER,
    )

    status = models.CharField(
        max_length=20,
        choices=ResourceStatus.choices,
        default=ResourceStatus.UNKNOWN,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name


class JobType(models.TextChoices):
    """
    Types of monitoring jobs.
    """

    CPU = "CPU", "CPU"
    MEMORY = "MEMORY", "Memory"
    DISK = "DISK", "Disk"
    API = "API", "API"
    WEBSITE = "WEBSITE", "Website"


class MonitoringJob(models.Model):
    """
    Represents a scheduled monitoring task.

    Example:
        Local Django API
            └── API Health Check (Every 60 seconds)

    APScheduler will later read this table
    to determine what jobs should run and when.
    """

    # ----------------------------------------------------------
    # Which server or monitored resource this job belongs to.
    #
    # One Server
    #      ↓
    # Many Monitoring Jobs
    # ----------------------------------------------------------
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name="monitoring_jobs",
    )

    # Friendly name shown in the dashboard and admin.
    # Example:
    # "API Health Check"
    name = models.CharField(max_length=100)

    # Type of monitoring that will be performed.
    #
    # Examples:
    # - CPU
    # - MEMORY
    # - DISK
    # - API
    # - WEBSITE
    job_type = models.CharField(
        max_length=20,
        choices=JobType.choices,
    )

    # How often this job should execute.
    #
    # Stored in seconds.
    #
    # Example:
    # 30  -> Every 30 seconds
    # 60  -> Every minute
    # 300 -> Every 5 minutes
    interval_seconds = models.PositiveIntegerField(
        default=60,
        help_text="Execution interval in seconds.",
    )

    # Allows administrators to pause monitoring
    # without deleting the job.
    enabled = models.BooleanField(default=True)

    # Timestamp of the previous execution.
    last_run = models.DateTimeField(
        null=True,
        blank=True,
    )

    # Timestamp of the next scheduled execution.
    next_run = models.DateTimeField(
        null=True,
        blank=True,
    )

    # Automatically set when the record is created.
    created_at = models.DateTimeField(auto_now_add=True)

    # Automatically updated whenever the record changes.
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Human-readable representation used in
        Django Admin and debugging.
        """
        return f"{self.server.name} - {self.name}"
