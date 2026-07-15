"""
Website Monitoring Service

This service monitors websites registered in EIAP.

Unlike API monitoring, which focuses on REST endpoints,
website monitoring verifies that public-facing websites
are reachable and responding correctly.

Current Features
----------------
• HTTP availability
• HTTP status code
• Response time measurement

Future Enhancements
-------------------
• Playwright browser automation
• Screenshot capture
• Login testing
• Page content validation
• SSL certificate monitoring
"""

# Used to measure request duration.
import time

# Used to perform HTTP requests.
import requests

# Used to generate timestamps.
from django.utils import timezone

# Import monitoring models.
from apps.monitoring.models import (
    Server,
    ResourceType,
    ResourceStatus,
    HealthCheck,
    HealthCheckStatus,
)


class WebsiteMonitor:
    """
    Service responsible for monitoring websites.
    """

    @staticmethod
    def check(url: str):
        """
        Perform a website availability check.

        Parameters
        ----------
        url : str
            Website URL.

        Returns
        -------
        dict
            Result of the website health check.
        """

        # ------------------------------------------
        # Record the start time.
        # ------------------------------------------
        start = time.perf_counter()

        try:

            # --------------------------------------
            # Send an HTTP GET request.
            # --------------------------------------
            response = requests.get(
                url,
                timeout=10,
            )

            # Record the finish time.
            end = time.perf_counter()

            return {

                # Website is considered online if
                # it responds with HTTP 200.
                "status": (
                    "ONLINE"
                    if response.status_code == 200
                    else "OFFLINE"
                ),

                # HTTP status code.
                "status_code": response.status_code,

                # Response time in milliseconds.
                "response_time": int(
                    (end - start) * 1000
                ),
            }

        except requests.RequestException:

            end = time.perf_counter()

            return {

                "status": "OFFLINE",

                "status_code": None,

                "response_time": int(
                    (end - start) * 1000
                ),
            }

    @staticmethod
    def monitor_all():
        """
        Monitor every registered website.

        This method is executed by the scheduler.

        Workflow

        Load Websites
                │
                ▼
        Perform HTTP Check
                │
                ▼
        Update Server Status
                │
                ▼
        Create HealthCheck
        """

        # ------------------------------------------------------
        # Retrieve every server configured as a WEBSITE.
        # ------------------------------------------------------
        websites = Server.objects.filter(
            resource_type=ResourceType.WEBSITE,
            is_active=True,
        )

        print(
            f"\nMonitoring {websites.count()} website(s)..."
        )

        # ------------------------------------------------------
        # Check every website individually.
        # ------------------------------------------------------
        for website in websites:

            print(
                f"Checking {website.host}"
            )

            # Perform the website health check.
            result = WebsiteMonitor.check(
                website.host
            )

            # Display the result.
            print(result)

            # --------------------------------------------------
            # Update the website status.
            # --------------------------------------------------
            if result["status"] == "ONLINE":

                website.status = ResourceStatus.ONLINE

            else:

                website.status = ResourceStatus.OFFLINE

            # Save the updated status.
            website.save()

            # --------------------------------------------------
            # Store the monitoring history.
            # --------------------------------------------------
            HealthCheck.objects.create(

                # Website that was monitored.
                server=website,

                # Website monitoring currently isn't linked
                # to a MonitoringJob.
                monitoring_job=None,

                # SUCCESS or FAILED.
                status=(
                    HealthCheckStatus.SUCCESS
                    if result["status"] == "ONLINE"
                    else HealthCheckStatus.FAILED
                ),

                # Record execution timestamps.
                started_at=timezone.now(),
                finished_at=timezone.now(),

                # Response time.
                execution_time_ms=result["response_time"],

                # HTTP status code.
                http_status=result["status_code"],
            )
