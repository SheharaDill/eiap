"""
Employee Search Workflow

Logs into OrangeHRM and searches
for an employee.
"""

from apps.browser.services.playwright_service import PlaywrightService

from apps.browser.pages.login_page import LoginPage
from apps.browser.pages.dashboard_page import DashboardPage
from apps.browser.pages.pim_page import PIMPage
from apps.browser.pages.employee_list_page import EmployeeListPage

from apps.browser.config.applications import ApplicationConfig
from apps.browser.config.credentials import DemoCredentials
from apps.browser.services.authentication_service import (
    AuthenticationService,
)


class EmployeeSearchWorkflow:
    """
    Executes an employee search.
    """

    @staticmethod
    def run():

        print("\n===================================")
        print("EMPLOYEE SEARCH WORKFLOW")
        print("===================================")

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

            # ------------------------------
            # Login
            # ------------------------------
            dashboard = AuthenticationService.login(
                page,
            )

            print("Dashboard loaded.")

            # ------------------------------
            # Open PIM
            # ------------------------------
            pim = PIMPage(page)

            pim.open()

            dashboard.wait(2000)

            # ------------------------------
            # Search Employee
            # ------------------------------
            employee = EmployeeListPage(page)

            employee.search_employee(
                "John"
            )
            employee.open_employee("John")

            dashboard.wait(3000)

            employee.take_results_screenshot(
                "employee_search.png"
            )

            print(
                "Employee search completed."
            )
        except Exception as e:

            print("\n========================")
            print("WORKFLOW FAILED")
            print("========================")
            print(e)

            raise

        finally:

            input(
                "\nPress Enter to close..."
            )

            PlaywrightService.close(
                playwright,
                browser,
            )
