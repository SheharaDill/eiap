"""
Management command to start the EIAP scheduler.

Run using:

    python manage.py run_scheduler

This command starts APScheduler and keeps it running until
the user stops it.
"""

# Allows us to create custom Django management commands.
from django.core.management.base import BaseCommand

# Used to keep the application alive.
import time

# Import our scheduler service.
from apps.scheduler.services.scheduler_service import SchedulerService


class Command(BaseCommand):
    """
    Starts the Enterprise Infrastructure Intelligence &
    Automation Platform scheduler.
    """

    # Help text displayed when running:
    #
    # python manage.py help run_scheduler
    help = "Starts the EIAP monitoring scheduler."

    def handle(self, *args, **options):
        """
        Entry point for the management command.
        """

        # Create the scheduler service.
        scheduler = SchedulerService()

        # Start APScheduler.
        scheduler.start()

        self.stdout.write(
            self.style.SUCCESS(
                "Scheduler is running. Press Ctrl+C to stop."
            )
        )

        try:
            # Keep the process alive forever.
            while True:
                time.sleep(1)

        except KeyboardInterrupt:

            self.stdout.write(
                self.style.WARNING(
                    "Stopping scheduler..."
                )
            )

            scheduler.shutdown()

            self.stdout.write(
                self.style.SUCCESS(
                    "Scheduler stopped successfully."
                )
            )
