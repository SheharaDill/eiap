"""
Browser API URLs

Defines REST API endpoints for browser automation.
"""

# Django URL routing.
from django.urls import path

# Browser API views.
from apps.browser.api.views import (
    WorkflowRunAPIView,
)

# ==========================================================
# Browser API Routes
# ==========================================================

urlpatterns = [

    #
    # Execute a browser workflow.
    #
    path(

        "browser/workflows/run/",

        WorkflowRunAPIView.as_view(),

        name="browser-workflow-run",

    ),

]
