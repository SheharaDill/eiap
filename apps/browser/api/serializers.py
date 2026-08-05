"""
Browser API Serializers

Defines serializers used by browser automation APIs.
"""

from rest_framework import serializers


class WorkflowRunSerializer(serializers.Serializer):
    """
    Request payload for running a browser workflow.
    """

    #
    # Workflow to execute.
    #
    workflow = serializers.CharField(
        max_length=100,
    )

    #
    # Optional employee information.
    #
    first_name = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    middle_name = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    last_name = serializers.CharField(
        required=False,
        allow_blank=True,
    )
