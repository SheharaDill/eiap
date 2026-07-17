"""
Add Employee Page

Represents the Add Employee screen.
"""

from apps.browser.pages.base_page import BasePage


class AddEmployeePage(BasePage):
    """
    Page Object for Add Employee.
    """

    def open(self):
        """
        Open the Add Employee page.
        """

        print("Opening Add Employee")

        self.page.get_by_role(
            "link",
            name="Add Employee",
        ).click()

    def enter_first_name(
        self,
        first_name: str,
    ):
        """
        Enter first name.
        """

        print(f"First Name : {first_name}")

        self.fill(
            'input[name="firstName"]',
            first_name,
        )

    def enter_middle_name(
        self,
        middle_name: str,
    ):
        """
        Enter middle name.
        """

        self.fill(
            'input[name="middleName"]',
            middle_name,
        )

    def enter_last_name(
        self,
        last_name: str,
    ):
        """
        Enter last name.
        """

        self.fill(
            'input[name="lastName"]',
            last_name,
        )

    def enable_login_details(self):
        """
        Enable account creation.
        """

        print("Enable Login Details")

        self.click(
            ".oxd-switch-input"
        )

    def enter_username(
        self,
        username: str,
    ):
        """
        Enter username.
        """

        self.fill(
            'input:below(label:text("Username"))',
            username,
        )

    def enter_password(
        self,
        password: str,
    ):
        """
        Enter password.
        """

        password_boxes = self.page.locator(
            'input[type="password"]'
        )

        password_boxes.nth(0).fill(password)

    def confirm_password(
        self,
        password: str,
    ):
        """
        Confirm password.
        """

        password_boxes = self.page.locator(
            'input[type="password"]'
        )

        password_boxes.nth(1).fill(password)

    def save(self):
        """
        Save employee.
        """

        print("Saving Employee")

        self.click(
            'button[type="submit"]'
        )

    def is_employee_created(self):
        """
        Verify that the employee was created.

        Returns
        -------
        bool
        """

        print("Verifying employee creation...")

        try:

            self.page.get_by_role(
                "heading",
                name="Personal Details",
            ).wait_for(
                timeout=10000,
            )

            print("Employee created successfully.")

            return True

        except Exception:

            print("Employee creation verification failed.")

            return False
