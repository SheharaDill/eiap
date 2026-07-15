"""
Browser Workflow Registry

This module acts as the central registry for every
browser automation workflow available in EIAP.

Instead of WorkflowRunner knowing every workflow,
it simply asks this registry for the requested
workflow.

This makes the automation framework easy to extend.

Adding a new workflow only requires:

1. Create workflow class.
2. Register it here.

No other code changes are needed.
"""

# Import available workflows.
from apps.browser.workflows.demo_workflow import DemoWorkflow


# ==========================================================
# Workflow Registry
# ==========================================================

WORKFLOWS = {

    # Demonstration workflow.
    "demo": DemoWorkflow,

}
