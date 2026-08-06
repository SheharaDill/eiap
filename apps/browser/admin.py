"""
Browser Admin

Registers Browser models with the Django Admin.
"""

from django.contrib import admin

from apps.browser.models import WorkflowExecution


@admin.register(WorkflowExecution)
class WorkflowExecutionAdmin(admin.ModelAdmin):
    """
    Admin configuration for WorkflowExecution.
    """

    list_display = (
        "workflow_name",
        "status",
        "started_at",
        "finished_at",
        "duration_seconds",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "workflow_name",
    )

    readonly_fields = (
        "started_at",
        "finished_at",
        "duration_seconds",
        "parameters",
        "error_message",
    )
