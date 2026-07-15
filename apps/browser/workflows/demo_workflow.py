"""
Demo Browser Workflow

This workflow demonstrates the browser automation
framework by opening a website and capturing
a screenshot.
"""

from apps.browser.services.playwright_service import (
    PlaywrightService,
)


class DemoWorkflow:
    """
    Simple demonstration workflow.
    """

    @staticmethod
    def run():
        """
        Execute the demo workflow.
        """

        print("\nRunning Demo Workflow...")

        playwright, browser, context, page = (
            PlaywrightService.open_website(
                url="https://example.com",
                headless=False,
            )
        )

        try:

            PlaywrightService.take_screenshot(
                page,
                "demo_workflow.png",
            )

            print("Demo workflow completed.")

        finally:

            PlaywrightService.close(
                playwright,
                browser,
            )
