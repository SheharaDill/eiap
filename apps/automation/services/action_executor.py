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

# Import the browser workflow runner.
#
# When an automation rule requests browser
# automation, the Action Executor delegates
# execution to the Workflow Runner.
from apps.browser.services.workflow_runner import (
    WorkflowRunner,
)


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
        # ------------------------------------------
        # Create Alert
        # ------------------------------------------
        #
        # Delegate alert creation to the AlertManager.
        #
        # AlertManager is responsible for:
        #
        # • Alert creation
        # • Alert deduplication
        # • Alert acknowledgement
        # • Alert resolution
        #
        # ActionExecutor simply decides which action
        # should be executed.
        #
        if rule.action == AutomationAction.CREATE_ALERT:

            # Import here to avoid circular imports.
            from apps.alerts.services.alert_manager import AlertManager

            # Delegate the work to AlertManager.
            AlertManager.create_alert(
                rule=rule,
                metric=metric,
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

            print(
                "Starting browser automation workflow..."
            )

            # Execute the registered browser workflow.
            #
            # For now we always run the demonstration
            # workflow.
            # Later this workflow name will be stored
            # in the database.
            WorkflowRunner.run(
                "demo",
            )

            return
