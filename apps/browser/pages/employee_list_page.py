"""
Employee List Page

Represents the Employee List screen
inside the PIM module.
"""

from apps.browser.pages.base_page import BasePage


class EmployeeListPage(BasePage):
    """
    Page Object for Employee List.
    """

    def search_employee(
        self,
        employee_name: str,
    ):
        """
        Search an employee by name.
        """

        print(
            f"Searching employee: {employee_name}"
        )

        # Click employee name textbox.

        textbox = self.page.get_by_role(
            "textbox",
            name="Type for hints...",
        ).first

        textbox.click()

        #
        # Type employee name.
        #
        textbox.fill(employee_name)

        #

        #
        # Click Search.
        #
        self.page.get_by_role(
            "button",
            name="Search",
        ).click()

        #
        # Wait for search results.
        #
        self.wait(3000)

    def open_employee(
        self,
        employee_name: str,
    ):
        """
        Open an employee from the search results.
        """

        print(
            f"Opening employee: {employee_name}"
        )

        #
        # Wait until search results appear.
        #
        self.wait(2000)

        #
        # Click the employee name.
        #
        self.page.get_by_text(
            employee_name,
            exact=True,
        ).first.click()

    def delete_employee(
        self,
        employee_name: str,
    ):
        """
        Delete a specific employee from the results table.
        """

        print(
            f"Deleting employee: {employee_name}"
        )

    #
        # Find the row containing the employee.
        #
        row = self.page.locator(
            "div.oxd-table-row"
        ).filter(
            has_text=employee_name,
        ).first

    #
        # Click Delete button in that row.
        #
        row.locator(
            "button"
        ).last.click()

        self.wait(1000)

    def confirm_delete(self):
        """
        Confirm employee deletion.
        """

        print(
            "Confirming deletion"
        )

        self.page.get_by_role(
            "button",
            name="Yes, Delete",
        ).click()

        self.wait(3000)

    def verify_deleted(self):
        """
        Verify employee deletion.
        """
        print("Waiting for success message...")

        try:

            self.page.get_by_text(
                "Successfully Deleted"
            ).wait_for(
                timeout=10000,
            )
            print("Success message found.")

            return True

        except Exception as e:

            print("Verification failed:")
            print(e)

            return False

    def clear_search(self):
        """
        Reset the search form.
        """

        print("Clearing search")

        self.click(

            'button[type="reset"]',

        )

    def take_results_screenshot(
        self,
        filename: str,
    ):
        """
        Capture the search results.
        """

        self.screenshot(filename)
