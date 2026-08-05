"""
Add Employee Workflow

Logs into OrangeHRM and creates
a new employee.
"""

from apps.browser.services.playwright_service import PlaywrightService

from apps.browser.services.authentication_service import (
    AuthenticationService,
)

from apps.browser.pages.pim_page import PIMPage
from apps.browser.pages.add_employee_page import AddEmployeePage

from apps.browser.config.applications import ApplicationConfig


class AddEmployeeWorkflow:
    """
    Creates a new employee.
    """

    @staticmethod
    def run(
        first_name: str = "John",
        middle_name: str = "A",
        last_name: str = "Smith",
    ):

        print("\n===================================")
        print("ADD EMPLOYEE WORKFLOW")
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

            # ------------------------
            # Login
            # ------------------------

            dashboard = AuthenticationService.login(

                page,

            )

            print(
                "Dashboard loaded."
            )

            # ------------------------
            # Open PIM
            # ------------------------

            pim = PIMPage(page)

            pim.open()

            dashboard.wait(2000)

            # ------------------------
            # Add Employee
            # ------------------------

            employee = AddEmployeePage(page)

            employee.open()

            dashboard.wait(2000)

            #
            # Enter employee details.
            #
            print(
                f"First Name : {first_name}"
            )

            employee.enter_first_name(

                first_name,

            )

            employee.enter_middle_name(

                middle_name,

            )

            employee.enter_last_name(

                last_name,

            )
            #
            # Generate a unique employee ID.
            #
            employee.enter_employee_id()

            #
            # Save employee.
            #
            employee.save()

            #
            # Debugging information.
            #
            print(
                "Current URL:",
                page.url,
            )

            page.pause()

            #
            # Verify employee creation.
            #
            if not employee.is_employee_created():

                raise Exception(
                    "Employee creation failed."
                )

            #
            # Capture screenshot.
            #
            employee.screenshot(

                "employee_created.png",

            )

            print(
                "Workflow completed successfully."
            )

        except Exception as error:

            print(error)

            raise

        finally:

            input(
                "\nPress Enter to close..."
            )

            PlaywrightService.close(

                playwright,

                browser,

            )
