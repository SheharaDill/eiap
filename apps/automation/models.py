"""
Automation models for EIAP.

This module defines the rules that determine when
automatic actions should be executed.

Example:

IF CPU > 90%

THEN Restart Service

These rules are stored in the database instead of
being hardcoded in Python.

This allows administrators to create, edit and disable
automation without changing application code.
"""

from django.db import models

from apps.monitoring.models import Server


# ==========================================================
# Metric Types
# ==========================================================
#
# Represents the type of metric that a rule evaluates.
#
# ==========================================================

class MetricType(models.TextChoices):
    """
    Types of metrics that can trigger automation.
    """

    CPU = "CPU", "CPU Usage"
    MEMORY = "MEMORY", "Memory Usage"
    DISK = "DISK", "Disk Usage"
    API = "API", "API Response Time"
    WEBSITE = "WEBSITE", "Website Response Time"


# ==========================================================
# Comparison Operators
# ==========================================================
#
# Defines how a metric should be compared to a threshold.
#
# Example:
#
# CPU > 90
#
# Metric: CPU
# Operator: >
# Threshold: 90
#
# ==========================================================

class ComparisonOperator(models.TextChoices):
    """
    Supported comparison operators.
    """

    GREATER_THAN = ">", "Greater Than (>)"
    LESS_THAN = "<", "Less Than (<)"
    GREATER_EQUAL = ">=", "Greater Than or Equal (>=)"
    LESS_EQUAL = "<=", "Less Than or Equal (<=)"
    EQUAL = "==", "Equal (==)"


# ==========================================================
# Automation Actions
# ==========================================================
#
# Defines what should happen when a rule matches.
#
# ==========================================================

class AutomationAction(models.TextChoices):
    """
    Available automation actions.
    """

    CREATE_ALERT = "CREATE_ALERT", "Create Alert"

    SEND_EMAIL = "SEND_EMAIL", "Send Email"

    RETRY_API = "RETRY_API", "Retry API"

    RESTART_SERVICE = "RESTART_SERVICE", "Restart Service"

    BROWSER_AUTOMATION = (
        "BROWSER_AUTOMATION",
        "Run Browser Automation",
    )


# ==========================================================
# Automation Rule Model
# ==========================================================

class AutomationRule(models.Model):
    """
    Represents a configurable automation rule.

    Example

    IF CPU > 90

    THEN Restart Service
    """

    # Friendly rule name.
    name = models.CharField(
        max_length=150,
    )

    # Server this rule belongs to.
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name="automation_rules",
    )

    # Metric to evaluate.
    metric_type = models.CharField(
        max_length=20,
        choices=MetricType.choices,
    )

    # Comparison operator.
    operator = models.CharField(
        max_length=2,
        choices=ComparisonOperator.choices,
    )

    # Threshold value.
    threshold = models.FloatField()

    # Action to execute.
    action = models.CharField(
        max_length=50,
        choices=AutomationAction.choices,
    )

    # Determines execution order.
    priority = models.PositiveIntegerField(
        default=1,
    )

    # Prevents repeated execution.
    cooldown_seconds = models.PositiveIntegerField(
        default=300,
    )

    # Enable / Disable rule.
    enabled = models.BooleanField(
        default=True,
    )

    # Record timestamps.
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        """
        Model configuration.
        """

        ordering = (
            "priority",
            "name",
        )

    def __str__(self):
        """
        Human-readable representation.
        """

        return (
            f"{self.name} "
            f"({self.metric_type} "
            f"{self.operator} "
            f"{self.threshold})"
        )
