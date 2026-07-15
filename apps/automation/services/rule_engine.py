"""
Rule Engine Service

This service is responsible for evaluating automation rules
against newly collected monitoring metrics.

Workflow

Metric Collected
        │
        ▼
Load Enabled Rules
        │
        ▼
Evaluate Rules
        │
        ▼
Rule Matched?
        │
   Yes ─────► Execute Action
        │
        ▼
   Continue
"""

# Import the automation rule model.
from apps.automation.models import (
    AutomationRule,
    ComparisonOperator,
    MetricType,
)

# Import the Metric model.
from apps.monitoring.models import Metric

# Import the Action Executor.
#
# Once a rule matches, the Rule Engine delegates
# execution to this service.
from apps.automation.services.action_executor import ActionExecutor
# Import the Alert Manager.
#
# This service manages the complete lifecycle
# of alerts including:
#
# • Creating alerts
# • Resolving alerts
# • Finding open alerts
# • Acknowledging alerts
#
from apps.alerts.services.alert_manager import AlertManager


class RuleEngine:
    """
    Evaluates automation rules.

    The Rule Engine is responsible only for deciding
    whether a rule matches.

    It does NOT perform the action itself.
    """

    @staticmethod
    def evaluate(metric: Metric):
        """
        Evaluate every enabled automation rule
        for the server that produced this metric.
        """

        # ------------------------------------------
        # Load enabled rules for this server.
        # ------------------------------------------
        rules = AutomationRule.objects.filter(
            server=metric.server,
            enabled=True,
        ).order_by("priority")

        print(
            f"\nEvaluating {rules.count()} automation rule(s)..."
        )

        # Evaluate every rule.
        for rule in rules:

            matched = RuleEngine.rule_matches(
                metric,
                rule,
            )

            if matched:

                print(
                    f"[MATCH] {rule.name}"
                )

                # We will execute the action later.
                print(
                    f"Action to execute: {rule.action}"
                )
                # Execute the configured automation action.
                ActionExecutor.execute(
                    rule,
                    metric,
                )

            else:

                print(
                    f"[NO MATCH] {rule.name}"
                )
                # ------------------------------------------
                # The rule no longer matches.
                #
                # If an OPEN alert exists for this rule,
                # automatically resolve it.
                # ------------------------------------------

                open_alert = AlertManager.find_open_alert(
                    server=metric.server,
                    rule=rule,
                )

                # Resolve the alert only if one exists.
                if open_alert:

                    AlertManager.resolve_alert(
                        alert=open_alert,
                        notes=(
                            "Resolved automatically because "
                            "the monitored metric returned "
                            "to a healthy value."
                        ),
                    )

    @staticmethod
    def rule_matches(metric: Metric, rule: AutomationRule):
        """
        Determine whether a rule matches.
        """

        # ------------------------------------------
        # Determine which metric value should
        # be evaluated.
        # ------------------------------------------

        if rule.metric_type == MetricType.CPU:
            value = metric.cpu_usage

        elif rule.metric_type == MetricType.MEMORY:
            value = metric.memory_usage

        elif rule.metric_type == MetricType.DISK:
            value = metric.disk_usage

        else:
            return False

        # ------------------------------------------
        # Compare the value against the threshold.
        # ------------------------------------------

        if rule.operator == ComparisonOperator.GREATER_THAN:
            return value > rule.threshold

        if rule.operator == ComparisonOperator.LESS_THAN:
            return value < rule.threshold

        if rule.operator == ComparisonOperator.GREATER_EQUAL:
            return value >= rule.threshold

        if rule.operator == ComparisonOperator.LESS_EQUAL:
            return value <= rule.threshold

        if rule.operator == ComparisonOperator.EQUAL:
            return value == rule.threshold

        return False
