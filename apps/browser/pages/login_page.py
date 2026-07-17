"""
Login Page

Represents the login screen of a web application.

This class follows the Page Object Model (POM)
design pattern.

Every interaction with the login page is defined
here.
"""

# Import the reusable BasePage.
#
# Every page object in the framework inherits
# common browser actions from this class.
from apps.browser.pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object representing a login page.
    """

    def open(self, url: str):
        """
        Open the application's login page.

        Instead of directly calling
        self.page.goto(),

        we reuse the implementation already
        provided by BasePage.
        """

        super().open(url)

    def login(
        self,
        username: str,
        password: str,
    ):
        """
        Log into the application.
        Perform login to OrangeHRM

        Parameters
        ----------
        username

            Username or email.

        password

            User password.
        """

        # ------------------------------------------
        # Enter username.
        #
        # Uses BasePage.fill()
        # ------------------------------------------
        self.fill(
            'input[name="username"]',
            username,
        )

        # ------------------------------------------
        # Enter password.
        #
        # Uses BasePage.fill()
        # ------------------------------------------
        self.fill(
            'input[name="password"]',
            password,
        )

        # ------------------------------------------
        # Click Login button.
        #
        # Uses BasePage.click()
        # ------------------------------------------
        self.click(
            'button[type="submit"]',
        )
