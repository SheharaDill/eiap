"""
Workflow Runner

Responsible for executing browser workflows.

The Workflow Runner does not know how each workflow
works.

Instead it loads the requested workflow from the
Workflow Registry.
"""

from apps.browser.workflow_registry import WORKFLOWS
#
# Workflow execution tracking.
#
from apps.browser.services.workflow_execution_service import (
    WorkflowExecutionService,
)


class WorkflowRunner:
    """
    Executes registered browser workflows.
    """

    @staticmethod
    def run(
        workflow_name: str,
        **kwargs,
    ):
        """
        Execute a browser workflow.

        Parameters
        ----------
        workflow_name : str

            Name of the workflow.

        **kwargs

            Optional parameters forwarded
            to the workflow.
        """
        #
        # Find the requested workflow.
    #
        workflow = WORKFLOWS.get(

            workflow_name,

        )

        if workflow is None:

            raise ValueError(

                f"Unknown workflow: {workflow_name}"

            )

        #
        # Create execution record.
        #
        execution = WorkflowExecutionService.start(

            workflow_name=workflow_name,

            parameters=kwargs,

        )
        try:

            #
            # Execute workflow.
            #
            workflow.run(

                **kwargs,

            )
            #
            # Mark workflow as successful.
            #
            WorkflowExecutionService.complete(

                execution,

            )
        except Exception as error:

           #
            # Mark workflow as failed.
            #
            WorkflowExecutionService.fail(

                execution,

                error,

            )

            #
            # Re-raise the exception so the API
            # can return an error response.
            #
            raise
