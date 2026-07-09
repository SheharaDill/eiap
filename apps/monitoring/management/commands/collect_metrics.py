"""
Django Management Command

Collects infrastructure metrics from every active server.

Usage:

    python manage.py collect_metrics

This command is intentionally separated from the scheduler.

Today:
    Developer executes it manually.

Later:
    APScheduler will execute it automatically.
"""

from django.core.management.base import BaseCommand

from apps.monitoring.models import Server
from apps.monitoring.services.metric_collector import MetricCollector


class Command(BaseCommand):
    """
    Custom Django management command.

    Collects metrics for every active server.
    """

    # Message displayed by Django.
    help = "Collect infrastructure metrics."

    def handle(self, *args, **options):
        """
        Entry point for the management command.
        """

        self.stdout.write(
            self.style.SUCCESS(
                "\n========== Metric Collection Started ==========\n"
            )
        )

        # Retrieve all active servers.
        servers = Server.objects.filter(is_active=True)

        # If no servers exist, exit gracefully.
        if not servers.exists():
            self.stdout.write(
                self.style.WARNING(
                    "No active servers found."
                )
            )
            return

        # Process each server.
        for server in servers:

            metric = MetricCollector.collect_and_save_metrics(server)

            self.stdout.write(
                self.style.SUCCESS(
                    (
                        f"{server.name} | "
                        f"CPU={metric.cpu_usage}% | "
                        f"Memory={metric.memory_usage}% | "
                        f"Disk={metric.disk_usage}%"
                    )
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "\n========== Metric Collection Finished ==========\n"
            )
        )
