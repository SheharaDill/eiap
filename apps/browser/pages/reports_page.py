"""
Reports Page

Represents the Reports section of the application.

This page is responsible for interacting with report
generation and downloading functionality.

The ReportsPage follows the Page Object Model (POM)
design pattern.
"""

# Import the reusable BasePage.
from apps.browser.pages.base_page import BasePage


class ReportsPage(BasePage):
    """
    Page Object representing the Reports page.
    """

    # ==================================================
    # Verification
    # ==================================================

    def is_loaded(self) -> bool:
        """
        Verify the Reports page has loaded.

        Returns
        -------
        bool

            True if the Reports page is visible.
        """

        #
        # NOTE
        #
        # This selector is only a placeholder.
        # Replace it with the actual selector
        # when automating a real application.
        #

        return self.page.locator(
            "h1"
        ).is_visible()

    # ==================================================
    # Report Actions
    # ==================================================

    def download_report(
        self,
        filename: str,
    ):
        """
        Download a report.

        Parameters
        ----------
        filename

           Name used when saving
           the downloaded report.
        """

        print(
            f"Downloading report -> {filename}"
        )

        #
        # Wait until Playwright detects
        # a browser download.
        #
        with self.page.expect_download() as download_info:

            #
            # Click Download.
            #
            self.click(
                "#download-report"
            )

            # Retrieve the Download object.
            download = download_info.value

            # Save it locally.
            download.save_as(

                f"apps/browser/downloads/{filename}"

            )

            print(
                "Download completed successfully."
            )

    def refresh_reports(self):
        """
        Refresh the report list.
        """

        self.click(
            "#refresh-reports"
        )

    def search_report(
        self,
        report_name: str,
    ):
        """
        Search for a report.

        Parameters
        ----------
        report_name

            Report name to search.
        """

        self.fill(
            "#report-search",
            report_name,
        )

    def open_report(
        self,
        report_name: str,
    ):
        """
        Open a report.

        Parameters
        ----------
        report_name

            Report name.

        NOTE

        Placeholder implementation.

        Later we'll replace this with
        a dynamic Playwright locator.
        """

        print(
            f"Opening report: {report_name}"
        )

        self.click(
            ".report-row"
        )
