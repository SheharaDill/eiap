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
from apps.browser.workflows.demo_workflow import DemoWorkflow
from apps.browser.workflows.login_workflow import LoginWorkflow
from apps.browser.workflows.employee_search_workflow import (
    EmployeeSearchWorkflow,
)
from apps.browser.workflows.add_employee_workflow import (
    AddEmployeeWorkflow,
)
# ==========================================================
# Workflow Registry
# ==========================================================

WORKFLOWS = {

    # Demonstration workflow.
    "demo": DemoWorkflow,
    "login": LoginWorkflow,
    "employee_search": EmployeeSearchWorkflow,
    "add_employee": AddEmployeeWorkflow,

}
