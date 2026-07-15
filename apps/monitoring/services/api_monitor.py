"""
API Monitoring Service

This service is responsible for monitoring REST APIs.

Unlike MetricCollector, which collects metrics from the
local operating system, this service performs HTTP requests
to determine whether an API is healthy.

Information collected includes:

• HTTP Status Code
• Response Time
• Availability

Later this service will also support:

• Authentication
• Custom Headers
• JSON Validation
• SSL Certificate Checks
• Retry Logic
• Timeout Handling
"""

# Used to measure execution time.
import time

# Used to perform HTTP requests.
import requests

# Django timezone.
from django.utils import timezone

# Monitoring models.
from apps.monitoring.models import (
    Server,
    HealthCheck,
    HealthCheckStatus,
    ResourceStatus,
)


class APIMonitor:
    """
    Service responsible for monitoring REST APIs.
    """

    @staticmethod
    def check(url: str):
        """
        Check the health of an API endpoint.

        Parameters
        ----------
        url : str
            API endpoint to monitor.

        Returns
        -------
        dict

        Example

        {
            "status": "ONLINE",
            "status_code": 200,
            "response_time": 145
        }
        """

        # ------------------------------------------
        # Record when the request starts.
        # ------------------------------------------
        start = time.perf_counter()

        try:

            # --------------------------------------
            # Perform the HTTP GET request.
            #
            # timeout=10 prevents the scheduler from
            # waiting forever.
            # --------------------------------------
            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 "
                        "(KHTML, like Gecko) "
                        "Chrome/138.0 Safari/537.36"
                    )
                },
            )

            # Stop timing.
            end = time.perf_counter()

            return {

                # HTTP status code.
                "status_code": response.status_code,

                # API considered online if 200.
                "status": (
                    "ONLINE"
                    if response.status_code == 200
                    else "OFFLINE"
                ),

                # Convert seconds → milliseconds.
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
        Monitor every API registered in EIAP.
        """

        # Load every enabled API.
        api_servers = Server.objects.filter(
            resource_type="API",
            is_active=True,
        )

        print(
            f"\nMonitoring {api_servers.count()} API(s)..."
        )

        for server in api_servers:

            # Build the complete URL.
            url = (
                f"http://{server.host}:"
                f"{server.port}"
                f"{server.endpoint}"
            )

            print(f"Checking {url}")

            # ------------------------------------------------------
            # Perform the API health check.
            # ------------------------------------------------------
            result = APIMonitor.check(url)

            # Display the result in the console.
            print(result)

            # ------------------------------------------------------
# Update the current status of the server.
#
# ONLINE  -> API responded successfully.
# OFFLINE -> API request failed.
#
# This status is shown later in the dashboard
# and Django Admin.
            # ------------------------------------------------------
            if result["status"] == "ONLINE":

                server.status = ResourceStatus.ONLINE

            else:

                server.status = ResourceStatus.OFFLINE

            # Save the updated status.
            server.save()
            # ------------------------------------------------------
            # Record the API monitoring execution.
            # Every API check is stored so administrators can
            # review monitoring history later.
            # ------------------------------------------------------
            HealthCheck.objects.create(

                # The monitored server.
                server=server,

                # API monitoring is not currently linked to a
                # MonitoringJob, so leave this empty.
                monitoring_job=None,

                # SUCCESS if the API is online.
                status=(
                    HealthCheckStatus.SUCCESS
                    if result["status"] == "ONLINE"
                    else HealthCheckStatus.FAILED
                ),

                # Start and finish times.
                #
                # We currently record the same timestamp for both.
                # Later we'll capture the exact start time before
                # sending the HTTP request.
                started_at=timezone.now(),

                # send HTTP request

                finished_at=timezone.now(),

                # HTTP response time in milliseconds.
                execution_time_ms=result["response_time"],

                # HTTP status code.
                http_status=result["status_code"],
            )
