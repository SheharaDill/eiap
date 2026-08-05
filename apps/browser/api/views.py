"""
Browser API Views

Exposes REST endpoints for executing browser
automation workflows.
"""

# Django REST Framework.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Browser components.
from apps.browser.api.serializers import (
    WorkflowRunSerializer,
)

from apps.browser.services.workflow_runner import (
    WorkflowRunner,
)


class WorkflowRunAPIView(APIView):
    """
    Execute a browser workflow.

    Example

    POST /api/browser/workflows/run/
    """

    def post(self, request):
        """
        Execute a workflow.
        """

        #
        # Validate incoming JSON.
        #
        serializer = WorkflowRunSerializer(

            data=request.data,

        )

        serializer.is_valid(

            raise_exception=True,

        )

        #
        # Extract validated data.
        #
        data = serializer.validated_data

    #    workflow = data["workflow"]

        try:

            #
            # Extract workflow name.
            #
            workflow = data.pop(
                "workflow"
            )

            #
            # Execute workflow.
            #
            WorkflowRunner.run(

                workflow_name=workflow,

                **data,

            )

            #
            # Success response.
            #
            return Response(

                {
                    "success": True,
                    "workflow": workflow,
                    "parameters": data,
                    "message": f"Workflow '{workflow}' executed successfully.",
                },

                status=status.HTTP_200_OK,

            )

        except Exception as error:

            #
            # Failure response.
            #
            return Response(

                {
                    "success": False,
                    "message": str(error),
                },

                status=status.HTTP_500_INTERNAL_SERVER_ERROR,

            )
