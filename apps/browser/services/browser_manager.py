"""
Browser Manager

This service is responsible for creating and managing
Playwright browser instances.

Responsibilities
----------------
• Start Playwright
• Launch Chromium
• Create browser contexts
• Open new pages
• Close browser resources

The Browser Manager does NOT perform automation.
It only manages browser lifecycle.

Other services such as WorkflowRunner and
PlaywrightService will use this manager.
"""

# Import Playwright.
from playwright.sync_api import sync_playwright


class BrowserManager:
    """
    Manages Playwright browser instances.
    """

    @staticmethod
    def create_browser(
        headless=True,
        slow_mo=0,
    ):
        """
        Start Playwright and launch Chromium.

        Parameters
        ----------
        headless : bool
            True  -> Browser runs in the background.
            False -> Browser window is visible.

        Returns
        -------
        tuple
            (
                playwright,
                browser,
                context,
                page,
            )
        """

        # Start the Playwright engine.
        playwright = sync_playwright().start()

        # Launch Chromium.
        browser = playwright.chromium.launch(
            # Show or hide the browser.
            headless=headless,

            # Slow down Playwright actions.
            slow_mo=slow_mo,


        )

        # Create an isolated browser context.
        context = browser.new_context()

        # Open a new tab.
        page = context.new_page()

        return (
            playwright,
            browser,
            context,
            page,
        )

    @staticmethod
    def close_browser(
        playwright,
        browser,
    ):
        """
        Close all browser resources.

        Parameters
        ----------
        playwright
            Playwright engine.

        browser
            Chromium browser instance.
        """

        # Close Chromium.
        browser.close()

        # Stop Playwright.
        playwright.stop()
