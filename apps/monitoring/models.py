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

    # API endpoint or website path.
    #
    # Examples:
    # /
    # /health/
    # /api/v1/status/
    endpoint = models.CharField(
        max_length=255,
        default="/",
    )

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

# ==========================================================
# Health Check Status
# ==========================================================
#
# Represents the outcome of a monitoring execution.
#
# Every monitoring job should finish in one of these states.
#
# ==========================================================


class HealthCheckStatus(models.TextChoices):
    """
    Possible outcomes of a monitoring execution.
    """

    # Monitoring completed successfully.
    SUCCESS = "SUCCESS", "Success"

    # Monitoring failed because of an error.
    FAILED = "FAILED", "Failed"

    # Monitoring exceeded the allowed execution time.
    TIMEOUT = "TIMEOUT", "Timeout"

    # Monitoring was intentionally skipped.
    SKIPPED = "SKIPPED", "Skipped"


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

# ==========================================================
# Metric Model
# ==========================================================
#
# Stores every metric collected by the monitoring engine.
#
# The scheduler will periodically execute monitoring jobs
# and create one Metric record for each execution.
#
# Example:
#
# Local Machine
# CPU: 18%
# Memory: 52%
# Disk: 61%
#
# These records become the foundation for:
#
# • Dashboards
# • Automation Rules
# • AI Analysis
# • Reports
# • Alerts
#
# ==========================================================


class Metric(models.Model):
    """
    Represents a single set of metrics collected from
    a monitored resource.
    """

    # ----------------------------------------------------------
    # Server this metric belongs to.
    #
    # One Server
    #      ↓
    # Thousands of Metric records
    # ----------------------------------------------------------
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name="metrics",
    )

    # CPU usage percentage.
    #
    # Example:
    # 21.4
    cpu_usage = models.FloatField()

    # Memory usage percentage.
    memory_usage = models.FloatField()

    # Disk usage percentage.
    disk_usage = models.FloatField()

    # API response time (milliseconds).
    #
    # Only used for API and Website monitoring.
    response_time = models.FloatField(
        null=True,
        blank=True,
    )

    # Current health of the resource
    #
    # Examples:
    # Healthy
    # Warning
    # Critical
    status = models.CharField(
        max_length=30,
        default="Healthy",
    )

    # When these metrics were collected.
    collected_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        """
        Model configuration.
        """

        # Newest metrics appear first.
        ordering = ["-collected_at"]

        # Database indexes improve query performance,
        # especially when the Metric table grows to
        # thousands or millions of records.
        indexes = [
            models.Index(fields=["server"]),
            models.Index(fields=["collected_at"]),
        ]

    def __str__(self):
        """
        Human-readable representation.
        """
        return (
            f"{self.server.name} | "
            f"CPU: {self.cpu_usage}% | "
            f"Memory: {self.memory_usage}%"
        )
# ==========================================================
# Health Check Model
# ==========================================================
#
# Stores information about every monitoring execution.
#
# Unlike Metric, this model stores execution metadata,
# not infrastructure measurements.
#
# Example:
#
# Job Started
#        │
#        ▼
# Collect Metrics
#        │
#        ▼
# Job Finished
#        │
#        ▼
# Save HealthCheck
#
# ==========================================================


class HealthCheck(models.Model):
    """
    Stores the result of a monitoring execution.
    """

    # ----------------------------------------------------------
    # The monitored server.
    # ----------------------------------------------------------
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name="health_checks",
    )

    # ----------------------------------------------------------
    # The monitoring job that executed.
    # ----------------------------------------------------------
    monitoring_job = models.ForeignKey(
        MonitoringJob,
        on_delete=models.CASCADE,
        related_name="health_checks",
        null=True,
        blank=True,
    )

    # ----------------------------------------------------------
    # Result of the execution.
    # ----------------------------------------------------------
    status = models.CharField(
        max_length=20,
        choices=HealthCheckStatus.choices,
        default=HealthCheckStatus.SUCCESS,
    )

    # ----------------------------------------------------------
    # When execution started.
    # ----------------------------------------------------------
    started_at = models.DateTimeField()

    # ----------------------------------------------------------
    # When execution finished.
    # ----------------------------------------------------------
    finished_at = models.DateTimeField()

    # ----------------------------------------------------------
    # Total execution time.
    #
    # Stored in milliseconds.
    # ----------------------------------------------------------
    execution_time_ms = models.PositiveIntegerField()

    # ----------------------------------------------------------
    # HTTP response status.
    #
    # Used for API and Website monitoring.
    # ----------------------------------------------------------
    http_status = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    # ----------------------------------------------------------
    # Category of the error.
    #
    # Example:
    # TimeoutError
    # ConnectionError
    # AuthenticationError
    # ----------------------------------------------------------
    error_type = models.CharField(
        max_length=100,
        blank=True,
    )

    # ----------------------------------------------------------
    # Detailed error message.
    # ----------------------------------------------------------
    error_message = models.TextField(
        blank=True,
    )

    # ----------------------------------------------------------
    # Website screenshot path.
    #
    # This will be used later by Playwright.
    # ----------------------------------------------------------
    screenshot_path = models.CharField(
        max_length=500,
        blank=True,
    )

    # ----------------------------------------------------------
    # Record creation timestamp.
    # ----------------------------------------------------------
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        """
        Model configuration.
        """

        ordering = [
            "-started_at",
        ]

        indexes = [
            models.Index(fields=["server"]),
            models.Index(fields=["status"]),
            models.Index(fields=["started_at"]),
        ]

    def __str__(self):
        """
        Human-readable representation.
        """
        return (
            f"{self.server.name} | "
            f"{self.status} | "
            f"{self.started_at}"
        )
