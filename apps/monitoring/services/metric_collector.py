"""
Metric Collection Service

This module is responsible for collecting infrastructure
metrics from monitored resources.

Initially, it collects metrics from the local machine using
the psutil library.

Later this service will also support:

- Remote Servers
- REST APIs
- Websites
- Databases
- Docker Containers

Author:
Enterprise Infrastructure & Automation Platform (EIAP)
"""

import time

from django.utils import timezone
import psutil

from apps.monitoring.models import (
    HealthCheck,
    HealthCheckStatus,
    Metric,
    Server,
)
# Import the automation rule engine.
#
# After every successful metric collection,
# the Rule Engine evaluates whether any
# automation rules should be triggered.
# from apps.automation.services.rule_engine import RuleEngine


class MetricCollector:
    """
    Service responsible for collecting system metrics.

    This class hides the implementation details of metric
    collection from the rest of the application.

    Other parts of the system only need to call:

        MetricCollector.collect_local_metrics()

    They don't need to know how the values are collected.
    """

    @staticmethod
    def collect_local_metrics():
        """
        Collect CPU, memory and disk usage from
        the local machine.

        Returns
        -------
        dict
            Dictionary containing collected metrics.

        Example
        -------
        {
            "cpu_usage": 21.5,
            "memory_usage": 48.3,
            "disk_usage": 61.2,
        }
        """

        # --------------------------------------------------
        # Current CPU utilization percentage.
        # interval=1 measures usage over one second.
        # --------------------------------------------------
        cpu_usage = psutil.cpu_percent(interval=1)

        # --------------------------------------------------
        # Current memory utilization percentage.
        # --------------------------------------------------
        memory_usage = psutil.virtual_memory().percent

        # --------------------------------------------------
        # Current disk utilization percentage.
        #
        # On Windows, "/" automatically refers to the
        # current drive. Later we'll make this configurable.
        # --------------------------------------------------
        disk_usage = psutil.disk_usage("/").percent

        # Return all collected values.
        return {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage,
        }

    @staticmethod
    def collect_and_save_metrics(server: Server) -> Metric:
        """
        Collect metrics from the local machine and save both
        Metric and HealthCheck records.

        This method represents one complete monitoring execution.
        """

        # --------------------------------------------------
        # Record when monitoring started.
        # --------------------------------------------------
        started_at = timezone.now()

        # Start a high-precision timer.
        start_time = time.perf_counter()

        try:

            # ----------------------------------------------
            # Collect system metrics.
            # ----------------------------------------------
            metrics = MetricCollector.collect_local_metrics()

            # ----------------------------------------------
            # Save the collected metrics.
            # ----------------------------------------------
            metric = Metric.objects.create(
                server=server,
                cpu_usage=metrics["cpu_usage"],
                memory_usage=metrics["memory_usage"],
                disk_usage=metrics["disk_usage"],
                status="Healthy",
            )
            # --------------------------------------------------
            # Evaluate automation rules using the newly
            # collected metrics.
            # The Rule Engine will determine whether any
            # automation rule matches this Metric.## Example:
            # CPU > 90%
            # If the condition is true, the Rule Engine
            # will report the matching rule.
            # (The Action Executor will be connected later.)
            # --------------------------------------------------

            from apps.automation.services.rule_engine import RuleEngine
            # Evaluate automation rules for the newly collected metric.
            RuleEngine.evaluate(metric)

            # Stop timer.
            end_time = time.perf_counter()

            finished_at = timezone.now()

            # Convert seconds → milliseconds.
            execution_time_ms = int(
                (end_time - start_time) * 1000
            )

            # ----------------------------------------------
            # Save successful execution.
            # ----------------------------------------------
            HealthCheck.objects.create(
                server=server,
                status=HealthCheckStatus.SUCCESS,
                started_at=started_at,
                finished_at=finished_at,
                execution_time_ms=execution_time_ms,
            )

            return metric

        except Exception as exc:

            end_time = time.perf_counter()

            finished_at = timezone.now()

            execution_time_ms = int(
                (end_time - start_time) * 1000
            )

            # ----------------------------------------------
            # Record failed execution.
            # ----------------------------------------------
            HealthCheck.objects.create(
                server=server,
                status=HealthCheckStatus.FAILED,
                started_at=started_at,
                finished_at=finished_at,
                execution_time_ms=execution_time_ms,
                error_type=type(exc).__name__,
                error_message=str(exc),
            )

            # Re-raise the exception so Django can report it.
            raise
