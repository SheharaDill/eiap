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

        # Enter employee name.
        self.fill(

            'input[placeholder="Type for hints..."]',

            employee_name,

        )

        # Click Search.
        self.click(

            'button[type="submit"]',

        )

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
