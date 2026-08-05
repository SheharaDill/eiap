"""
Workflow Runner

Responsible for executing browser workflows.

The Workflow Runner does not know how each workflow
works.

Instead it loads the requested workflow from the
Workflow Registry.
"""

from apps.browser.workflow_registry import WORKFLOWS


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

        workflow = WORKFLOWS.get(

            workflow_name,

        )

        if workflow is None:

            raise ValueError(

                f"Unknown workflow: {workflow_name}"

            )

        #
        # Execute workflow.
        #
        workflow.run(

            **kwargs,

        )
