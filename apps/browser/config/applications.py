"""
Application Configuration

Stores URLs for every application
automated by the Playwright framework.

Keeping URLs here avoids hardcoding
them throughout workflows.
"""


class ApplicationConfig:
    """
    URLs for browser automation.
    """

    # ==========================================
    # OrangeHRM Demo
    # ==========================================

    ORANGE_HRM_URL = (
        "https://opensource-demo.orangehrmlive.com/"
    )

    # ==========================================
    # The Internet
    # ==========================================

    THE_INTERNET_URL = (
        "https://the-internet.herokuapp.com/"
    )

    # ==========================================
    # Sauce Demo
    # ==========================================

    SAUCE_DEMO_URL = (
        "https://www.saucedemo.com/"
    )

    # ==========================================
    # Demo QA
    # ==========================================

    DEMO_QA_URL = (
        "https://demoqa.com/"
    )
