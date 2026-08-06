"""
Workflow Execution Service

Responsible for creating and updating browser
workflow execution records.

This service provides a single place for tracking
workflow execution history.
"""

from django.utils import timezone

from apps.browser.models import WorkflowExecution


class WorkflowExecutionService:
    """
    Manages workflow execution history.
    """

    @staticmethod
    def start(
        workflow_name: str,
        parameters: dict,
    ):
        """
        Create a new execution record.

        Returns
        -------
        WorkflowExecution
        """

        return WorkflowExecution.objects.create(
            workflow_name=workflow_name,
            parameters=parameters,
            status=WorkflowExecution.Status.RUNNING,
        )

    @staticmethod
    def complete(
        execution: WorkflowExecution,
        screenshot: str = "",
    ):
        """
        Mark a workflow as successful.
        """

        execution.status = WorkflowExecution.Status.SUCCESS

        execution.finished_at = timezone.now()

        execution.screenshot = screenshot

        execution.duration_seconds = (
            execution.finished_at
            - execution.started_at
        ).total_seconds()

        execution.save()

    @staticmethod
    def fail(
        execution: WorkflowExecution,
        error: Exception,
    ):
        """
        Mark a workflow as failed.
        """

        execution.status = WorkflowExecution.Status.FAILED

        execution.finished_at = timezone.now()

        execution.error_message = str(error)

        execution.duration_seconds = (
            execution.finished_at
            - execution.started_at
        ).total_seconds()

        execution.save()
