"""
Delete Employee Workflow
"""

from apps.browser.services.playwright_service import PlaywrightService
from apps.browser.services.authentication_service import AuthenticationService

from apps.browser.pages.pim_page import PIMPage
from apps.browser.pages.employee_list_page import EmployeeListPage

from apps.browser.config.applications import ApplicationConfig


class DeleteEmployeeWorkflow:

    @staticmethod
    def run():

        print("\n===================================")
        print("DELETE EMPLOYEE WORKFLOW")
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

            #
            # Login
            #
            AuthenticationService.login(page)

            #
            # Open PIM
            #
            pim = PIMPage(page)

            pim.open()

            #
            # Search Employee
            #
            employees = EmployeeListPage(page)

            employees.search_employee(
                "John SD"
            )

            #
            # Delete Employee
            #
            # employees.delete_first_employee()
            employees.delete_employee(
                "John SD"
            )

            #
            # Confirm
            #
            employees.confirm_delete()

            employees.wait(3000)

            #
            # Verify
            #
            if employees.verify_deleted():

                print(
                    "Employee deleted successfully."
                )

            else:

                print(
                    "Employee deletion failed."
                )

            employees.screenshot(
                "employee_deleted.png"
            )

        finally:

            input(
                "\nPress Enter to close..."
            )

            PlaywrightService.close(
                playwright,
                browser,
            )
