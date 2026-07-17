"""
OrangeHRM Login Workflow
"""

from apps.browser.services.playwright_service import PlaywrightService

from apps.browser.pages.login_page import LoginPage
from apps.browser.pages.dashboard_page import DashboardPage

from apps.browser.config.applications import ApplicationConfig
from apps.browser.config.credentials import DemoCredentials


class LoginWorkflow:
    """
    Executes the OrangeHRM login workflow.
    """

    @staticmethod
    def run():

        print("\n===================================")
        print("ORANGEHRM LOGIN WORKFLOW")
        print("===================================")

        #
        # Open browser.
        #
        (
            playwright,
            browser,
            context,
            page,
        ) = PlaywrightService.open_website(

            ApplicationConfig.ORANGE_HRM_URL,

            headless=False,

        )

        try:

            login = LoginPage(page)

            dashboard = DashboardPage(page)

            #
            # Login.
            #
            login.login(

                DemoCredentials.USERNAME,

                DemoCredentials.PASSWORD,

            )

            #
            # Wait a little while the dashboard loads.
            #
            dashboard.wait(3000)

            #
            # Verify dashboard.
            #
            if dashboard.is_loaded():

                print(
                    "Login successful."
                )

            else:

                print(
                    "Dashboard not detected."
                )

            #
            # Capture screenshot.
            #
            PlaywrightService.take_screenshot(

                page,

                "orangehrm_dashboard.png",

            )

        finally:

            #
            # Close browser.
            #
            input(
                "\nPress Enter to close the browser..."
            )

            PlaywrightService.close(

                playwright,

                browser,

            )
