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
