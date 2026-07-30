"""
Alert Service

Handles the lifecycle of alerts.

Responsibilities

- Create alerts
- Resolve alerts
- Find open alerts
"""

from django.utils import timezone

from apps.alerts.models import Alert, AlertStatus


class AlertService:

    @staticmethod
    def resolve_alert(rule):
        """
        Resolve any open alert created by this rule.
        """

        alert = Alert.objects.filter(
            rule=rule,
            status=AlertStatus.OPEN,
        ).first()

        if not alert:
            return

        alert.status = AlertStatus.RESOLVED
        alert.resolved_at = timezone.now()
        alert.resolution_notes = (
            "Automatically resolved because "
            "the metric returned to a healthy state."
        )

        alert.save()

        print(
            f"Resolved alert #{alert.id}"
        )