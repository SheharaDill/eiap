"""
Edit Employee Workflow

Updates employee information.
"""

from apps.browser.services.playwright_service import PlaywrightService
from apps.browser.services.authentication_service import AuthenticationService

from apps.browser.pages.pim_page import PIMPage
from apps.browser.pages.employee_list_page import EmployeeListPage
from apps.browser.pages.employee_details_page import EmployeeDetailsPage

from apps.browser.config.applications import ApplicationConfig


class EditEmployeeWorkflow:

    @staticmethod
    def run():

        print("\n===================================")
        print("EDIT EMPLOYEE WORKFLOW")
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
            # Search employee
            #
            employees = EmployeeListPage(page)

            employees.search_employee(
                "John"
            )

            #
            # Open employee
            #
            employees.open_employee(
                "John"
            )

            #
            # Personal Details
            #
            details = EmployeeDetailsPage(page)

            #
            # Change Nationality
            #
            details.select_nationality(
                "Indian"
            )

            #
            # Change Marital Status
            #
            details.select_marital_status(
                "Single"
            )

            #
            # Save
            #
            details.save()

            #
            # Verify
            #
            if details.verify_updated():

                print(
                    "Employee updated successfully."
                )

            else:

                print(
                    "Employee update failed."
                )

            PlaywrightService.take_screenshot(

                page,

                "employee_updated.png",

            )

        finally:

            input(
                "\nPress Enter to close..."
            )

            PlaywrightService.close(

                playwright,

                browser,

            )
