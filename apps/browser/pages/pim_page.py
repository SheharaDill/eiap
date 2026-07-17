"""
PIM Page

Represents the Employee Management
section of OrangeHRM.
"""

from apps.browser.pages.base_page import BasePage


class PIMPage(BasePage):
    """
    Page Object for the PIM module.
    """

    def open(self):
        """
        Open the PIM module.
        """

        print("Opening PIM Module")

        self.click(
            'a[href*="pim"]'
        )

    def employee_list(self):
        """
        Open Employee List.
        """

        print("Opening Employee List")

        self.click(

            'a[href="/web/index.php/pim/viewEmployeeList"]'

        )
        print(self.page.url)
