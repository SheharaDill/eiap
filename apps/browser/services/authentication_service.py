"""
Authentication Service

Handles authentication for browser workflows.

Every workflow that requires login should use this
service instead of implementing login logic itself.
"""

from apps.browser.pages.login_page import LoginPage
from apps.browser.pages.dashboard_page import DashboardPage

from apps.browser.config.credentials import DemoCredentials


class AuthenticationService:
    """
    Handles login into OrangeHRM.
    """

    @staticmethod
    def login(page):
        """
        Login and verify dashboard.

        Parameters
        ----------
        page
            Active Playwright page.

        Returns
        -------
        DashboardPage
        """

        login_page = LoginPage(page)

        dashboard = DashboardPage(page)

        login_page.login(
            DemoCredentials.USERNAME,
            DemoCredentials.PASSWORD,
        )

        dashboard.wait(3000)

        if not dashboard.is_loaded():

            raise Exception(
                "Login failed."
            )

        print("Login successful.")

        return dashboard
