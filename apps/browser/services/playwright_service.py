"""
Playwright Service

This service contains reusable browser automation
operations used throughout EIAP.

Unlike BrowserManager, this class performs actual
browser interactions.

Examples

• Open URL
• Click buttons
• Fill forms
• Wait for elements
• Capture screenshots

Every browser workflow will use this service instead
of directly calling Playwright.
"""

# Used for working with file paths.
from pathlib import Path

# Import the Browser Manager.
from apps.browser.services.browser_manager import BrowserManager


class PlaywrightService:
    """
    High-level Playwright operations.

    This class wraps common browser actions into
    reusable methods.
    """

    @staticmethod
    def open_website(
        url: str,
        headless=False,
    ):
        """
        Open a website in Chromium.

        Parameters
        ----------
        url : str
            Website URL.

        headless : bool
            Whether Chromium should be visible.

        Returns
        -------
        tuple

        (
            playwright,
            browser,
            context,
            page
        )
        """

        # Create a browser.
        playwright, browser, context, page = (
            BrowserManager.create_browser(
                headless=headless,
                slow_mo=800,
            )
        )

        print(f"Opening {url}")

        # Navigate to the website.
        page.goto(
            url,
            wait_until="networkidle",
        )

        return (
            playwright,
            browser,
            context,
            page,
        )

    @staticmethod
    def take_screenshot(
        page,
        filename: str,
    ):
        """
        Capture a browser screenshot.

        Parameters
        ----------
        page
            Active Playwright page.

        filename : str
            Screenshot filename.
        """

        # Create screenshots directory if needed.
        screenshot_dir = Path(
            "apps/browser/screenshots"
        )

        screenshot_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Full screenshot path.
        path = screenshot_dir / filename

        # Capture screenshot.
        page.screenshot(
            path=str(path),
            full_page=True,
        )

        print(
            f"Screenshot saved -> {path}"
        )

        return str(path)

    @staticmethod
    def close(
        playwright,
        browser,
    ):
        """
        Close browser resources.
        """

        BrowserManager.close_browser(
            playwright,
            browser,
        )
