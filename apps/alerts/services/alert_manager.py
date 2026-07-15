"""
Alert Manager Service

This service centralizes every operation performed on
Alert objects.

Why?

Without an Alert Manager, alert-related logic would end up
spread across multiple modules:

- Action Executor
- Scheduler
- Rule Engine
- API Views

That quickly becomes difficult to maintain.

Instead, every alert operation passes through this service.

Responsibilities
----------------
✓ Create alerts
✓ Find open alerts
✓ Resolve alerts
✓ Reopen alerts
✓ Acknowledge alerts

This follows the Single Responsibility Principle (SRP)
and keeps the project modular.
"""

# ---------------------------------------------------------
# Django utilities
# ---------------------------------------------------------
from django.utils import timezone

# ---------------------------------------------------------
# Alert models
# ---------------------------------------------------------
from apps.alerts.models import (
    Alert,
    AlertSeverity,
    AlertStatus,
)


class AlertManager:
    """
    Central service responsible for managing the entire
    lifecycle of alerts.

    No other module should directly create or update Alert
    objects.

    Instead they should call:

        AlertManager.create_alert(...)
        AlertManager.resolve_alert(...)
        AlertManager.find_open_alert(...)
    """

    # ==========================================================
    # Create Alert
    # ==========================================================
    #
    # This method is responsible for creating a new alert.
    #
    # Before creating an alert, it first checks whether an
    # identical OPEN alert already exists.
    #
    # If one already exists, we simply return it instead of
    # creating duplicates.
    #
    # This is called "Alert Deduplication" and is used by
    # enterprise monitoring systems to prevent alert flooding.
    #
    # ==========================================================

    @staticmethod
    def create_alert(rule, metric):
        """
        Create a new alert if one does not already exist.

        Parameters
        ----------
        rule : AutomationRule
            The rule that matched.

        metric : Metric
            The metric that triggered the rule.

        Returns
        -------
        Alert
            The existing alert or the newly created alert.
        """

        # ------------------------------------------------------
        # Check whether an OPEN alert already exists.
        # ------------------------------------------------------
        existing_alert = AlertManager.find_open_alert(
            server=metric.server,
            rule=rule,
        )

        # ------------------------------------------------------
        # If an alert already exists, return it.
        # ------------------------------------------------------
        if existing_alert:

            print(
                f"Open alert already exists "
                f"(ID: {existing_alert.id})"
            )

            return existing_alert

        # ------------------------------------------------------
        # Create a brand-new alert.
        # ------------------------------------------------------
        alert = Alert.objects.create(

            # Server where the problem occurred.
            server=metric.server,

            # Rule that triggered the alert.
            rule=rule,

            # Metric responsible for the alert.
            metric=metric,

            # Friendly alert title.
            name=rule.name,

            # Detailed alert description.
            message=(
                f"{rule.metric_type} "
                f"{rule.operator} "
                f"{rule.threshold}"
            ),

            # Default severity.
            severity=AlertSeverity.WARNING,

            # Newly created alerts are OPEN.
            status=AlertStatus.OPEN,
        )

        print(
            f"Alert created successfully "
            f"(ID: {alert.id})"
        )

        return alert

    @staticmethod
    def find_open_alert(server, rule):
        """
        Return an existing OPEN alert.

        Parameters
        ----------
        server : Server
            Server that generated the alert.

        rule : AutomationRule
            Rule that generated the alert.

        Returns
        -------
        Alert | None
        """

        return Alert.objects.filter(
            server=server,
            rule=rule,
            status=AlertStatus.OPEN,
        ).first()

    @staticmethod
    def resolve_alert(alert, notes="Resolved automatically"):
        """
        Resolve an existing alert.

        Parameters
        ----------
        alert : Alert

        notes : str
            Optional resolution message.
        """

        # Update status.
        alert.status = AlertStatus.RESOLVED

        # Store resolution timestamp.
        alert.resolved_at = timezone.now()

        # Save notes.
        alert.resolution_notes = notes

        # Persist changes.
        alert.save()

        print(
            f"Alert #{alert.id} resolved."
        )

    @staticmethod
    def acknowledge_alert(alert, user):
        """
        Mark an alert as acknowledged.

        Parameters
        ----------
        alert : Alert

        user : User
            User acknowledging the alert.
        """

        alert.status = AlertStatus.ACKNOWLEDGED

        alert.acknowledged_by = user

        alert.acknowledged_at = timezone.now()

        alert.save()

        print(
            f"Alert #{alert.id} acknowledged."
        )
