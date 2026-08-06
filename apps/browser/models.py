"""
Browser Models

Stores browser automation execution history.
"""

from django.db import models


class WorkflowExecution(models.Model):
    """
    Stores every browser workflow execution.
    """

    class Status(models.TextChoices):
        """
        Execution status.
        """

        PENDING = "PENDING", "Pending"
        RUNNING = "RUNNING", "Running"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    #
    # Workflow information
    #

    workflow_name = models.CharField(
        max_length=100,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    #
    # Timing
    #

    started_at = models.DateTimeField(
        auto_now_add=True,
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    duration_seconds = models.FloatField(
        null=True,
        blank=True,
    )

    #
    # Request parameters
    #

    parameters = models.JSONField(
        default=dict,
        blank=True,
    )

    #
    # Output
    #

    screenshot = models.CharField(
        max_length=255,
        blank=True,
    )

    error_message = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = [
            "-started_at",
        ]

    def __str__(self):
        return (
            f"{self.workflow_name} "
            f"({self.status})"
        )
