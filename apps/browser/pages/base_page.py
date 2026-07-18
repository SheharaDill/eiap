"""
Base Page

Every page inside the Playwright framework inherits
from this class.

The BasePage stores the Playwright Page object and
provides reusable browser actions.

Benefits

• Eliminates duplicate code
• Easier maintenance
• Consistent browser interactions
• Enterprise Page Object Model (POM)
"""
from pathlib import Path


class BasePage:
    """
    Parent class for every browser page.

    Every page object (LoginPage, DashboardPage,
    SettingsPage, etc.) inherits from BasePage.
    """

    def __init__(self, page):
        """
        Store the Playwright Page instance.

        Parameters
        ----------
        page

            Playwright Page object.
        """

        self.page = page

    # ==================================================
    # Navigation
    # ==================================================

    def open(self, url: str):
        """
        Navigate to a web page.

        Parameters
        ----------
        url

            URL to open.
        """

        print(f"Opening {url}")

        self.page.goto(url)

    # ==================================================
    # Mouse Actions
    # ==================================================

    def click(self, selector: str):
        """
        Click an element.

        Parameters
        ----------
        selector

            CSS selector.
        """

        print(f"Clicking: {selector}")

        self.page.click(selector)

    # ==================================================
    # Keyboard Actions
    # ==================================================

    def fill(
        self,
        selector: str,
        value: str,
    ):
        """
        Fill a textbox.

        Parameters
        ----------
        selector

            CSS selector.

        value

            Text to enter.
        """

        print(
            f"Typing '{value}' into {selector}"
        )

        self.page.fill(
            selector,
            value,
        )

    # ==================================================
    # Waiting
    # ==================================================

    def wait(
        self,
        milliseconds: int,
    ):
        """
        Pause execution.

        Parameters
        ----------
        milliseconds

            Wait time.
        """

        print(
            f"Waiting {milliseconds} ms"
        )

        self.page.wait_for_timeout(
            milliseconds,
        )

    # ==================================================
    # Screenshots
    # ==================================================

    def screenshot(
        self,
        filename: str,
    ):
        """
        Capture a screenshot.
        """
        screenshot_dir = Path(
            "apps/browser/screenshots"
        )

        screenshot_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = screenshot_dir / filename

        print(
            f"Saving screenshot -> {path}"
        )

        self.page.screenshot(
            path=str(path),
            full_page=True,
        )

    # ==================================================
    # Browser Information
    # ==================================================

    def title(self):
        """
        Return the page title.
        """

        return self.page.title()

    def current_url(self):
        """
        Return the current URL.
        """

        return self.page.url
