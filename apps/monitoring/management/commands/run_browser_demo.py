"""
Run Browser Demo

Management command used to test the Playwright
automation framework independently.
"""

from django.core.management.base import BaseCommand

from apps.browser.services.workflow_runner import (
    WorkflowRunner,
)


class Command(BaseCommand):
    """
    Django management command.
    """

    help = "Runs the Playwright demo workflow."

    def handle(self, *args, **kwargs):

        WorkflowRunner.run(
            #    "add_employee",
            "employee_search",
        )
