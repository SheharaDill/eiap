"""
Browser Configuration

Contains browser-related settings
used by the Playwright framework.
"""


class BrowserConfig:
    """
    Browser settings.
    """

    # Launch browser in headless mode.
    HEADLESS = False

    # Slow down browser actions.
    #
    # Useful during development.
    SLOW_MO = 300

    # Default timeout (milliseconds).
    TIMEOUT = 30000
