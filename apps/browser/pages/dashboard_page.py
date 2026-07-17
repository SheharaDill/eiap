"""
Dashboard Page

Represents the application's dashboard after a
successful login.

Every interaction with the dashboard belongs here.

The DashboardPage follows the Page Object Model
(POM) design pattern.
"""

# Import the reusable BasePage.
from apps.browser.pages.base_page import BasePage


class DashboardPage(BasePage):
    """
    Page Object representing the application's dashboard.
    """

    # ==================================================
    # Verification
    # ==================================================

    def is_loaded(self) -> bool:
        """
        Verify that the dashboard has loaded.

        Returns
        -------
        bool

            True if the dashboard appears to be loaded.
        """

        #
        # NOTE
        #
        # This selector is only a placeholder.
        #
        # Later we will replace it with the actual
        # application's dashboard selector.
        #

        return self.page.locator(
            "h6"
        ).is_visible()

    # ==================================================
    # Navigation
    # ==================================================

    def open_reports(self):
        """
        Open the Reports section.
        """

        self.click(
            "#reports-menu"
        )

    def open_users(self):
        """
        Open the Users section.
        """

        self.click(
            "#users-menu"
        )

    def open_settings(self):
        """
        Open the Settings section.
        """

        self.click(
            "#settings-menu"
        )

    # ==================================================
    # Authentication
    # ==================================================

    def logout(self):
        """
        Logout from the application.
        """

        self.click(
            "#logout-button"
        )
