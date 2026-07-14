"""
Action Executor Service

This service performs the actions requested by the
Rule Engine.

The Rule Engine decides WHAT should happen.

The Action Executor performs the action.

Example

CPU > 90%

↓

Rule Matches

↓

Action Executor

↓

Create Alert
"""

# Import the automation action enumeration.
from apps.automation.models import AutomationAction

# Import the Alert model and related enumerations.
#
# These are used to create real alert records in the database.
from apps.alerts.models import (
    Alert,
    AlertSeverity,
    AlertStatus,
)

# Import Metric so we can attach the alert to the
# metric that triggered it.
from apps.monitoring.models import Metric


class ActionExecutor:
    """
    Executes automation actions.

    Initially this service only simulates actions.

    Later it will integrate with:

    - Alerts
    - Email
    - Playwright
    - REST APIs
    - Docker
    - Windows Services
    """

    @staticmethod
    def execute(rule, metric: Metric):
        """
        Execute the action configured for an
        Automation Rule.

        Parameters
        ----------
        rule : AutomationRule
            The rule that matched.
        """

        print("\n===================================")
        print("ACTION EXECUTOR")
        print("===================================")

        # ------------------------------------------
        # Create Alert
        # ------------------------------------------
        if rule.action == AutomationAction.CREATE_ALERT:

            # Check whether an OPEN alert already exists
            # for this server and rule.
            existing_alert = Alert.objects.filter(
                server=rule.server,
                rule=rule,
                status=AlertStatus.OPEN,
            ).first()

            # If an alert already exists, don't create another.
            if existing_alert:

                print(
                    f"Open alert already exists "
                    f"(ID: {existing_alert.id})"
                )

                return

            # Create a new Alert record in the database.
            alert = Alert.objects.create(

                # Server where the incident occurred.
                server=metric.server,

                # Rule that triggered the alert.
                rule=rule,

                # Metric responsible for triggering the rule.
                metric=metric,

                # Short alert title.
                name=rule.name,

                # Human-readable description.
                message=(
                    f"Automation rule '{rule.name}' "
                    f"was triggered."
                ),

                # Default severity.
                severity=AlertSeverity.WARNING,
                status=AlertStatus.OPEN,
            )

            print(
                f"Alert created successfully "
                f"(ID: {alert.id})"
            )

            return

        # ------------------------------------------
        # Send Email
        # ------------------------------------------
        if rule.action == AutomationAction.SEND_EMAIL:

            print("Sending Email...")

            return

        # ------------------------------------------
        # Retry API
        # ------------------------------------------
        if rule.action == AutomationAction.RETRY_API:

            print("Retrying API...")

            return

        # ------------------------------------------
        # Restart Service
        # ------------------------------------------
        if rule.action == AutomationAction.RESTART_SERVICE:

            print("Restarting Service...")

            return

        # ------------------------------------------
        # Browser Automation
        # ------------------------------------------
        if rule.action == AutomationAction.BROWSER_AUTOMATION:

            print("Launching Browser Automation...")

            return

        print("Unknown automation action.")
