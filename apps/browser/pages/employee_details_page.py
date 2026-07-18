"""
Employee Details Page

Represents the Personal Details page of an employee.

Responsible for editing employee information.
"""

from apps.browser.pages.base_page import BasePage


class EmployeeDetailsPage(BasePage):
    """
    Page Object for Employee Details.
    """

    def is_loaded(self):
        """
        Verify Personal Details page.
        """

        return "viewPersonalDetails" in self.page.url

    def select_nationality(
            self,
            nationality: str,
    ):
        """
        Select employee nationality.

        Implementation coming next.
        """

        print(
            f"Selecting nationality: {nationality}"
        )

       #
       # Open the first dropdown on the page.
       #
        self.page.locator(
            ".oxd-icon.bi-caret-down-fill.oxd-select-text--arrow"
        ).first.click()

        #
        # Select nationality.
        #
        self.page.get_by_role(
            "option",
            name=nationality,
        ).click()

    def select_marital_status(
        self,
        status: str,
    ):
        """
        Select employee marital status.
        """

        print(
            f"Selecting marital status: {status}"
        )

        #
        # The second dropdown is Marital Status.
        #
        self.page.locator(
            ".oxd-icon.bi-caret-down-fill.oxd-select-text--arrow"
        ).nth(1).click()

        self.page.get_by_role(
            "option",
            name=status,
        ).click()

    def save(self):
        """
        Save employee details.
        """

        print("Saving employee details...")

        self.page.get_by_role(
            "button",
            name="Save",
        ).first.click()

    def verify_updated(self):
        """
        Verify update was successful.
         """

        try:

            self.page.get_by_text(
                "Successfully Updated",
            ).wait_for(
                timeout=10000,
            )

            return True

        except Exception:

            return False
