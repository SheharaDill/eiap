"""
Scheduler service for the Enterprise Infrastructure Intelligence
& Automation Platform (EIAP).

This service is responsible for:

1. Creating the APScheduler instance.
2. Registering monitoring jobs.
3. Executing monitoring tasks automatically.
4. Keeping the scheduler running.

The scheduler is the heart of the automation platform because
it removes the need for administrators to manually execute
monitoring commands.

Instead of:

python manage.py collect_metrics

the scheduler automatically executes monitoring jobs
at configured intervals.

Example:

Every 60 Seconds
        │
        ▼
Metric Collector
        │
        ▼
Save Metric
        │
        ▼
Save HealthCheck
"""

# Import APScheduler's background scheduler.
#
# BackgroundScheduler runs jobs in the background while
# allowing Django to continue running normally.
from apscheduler.schedulers.background import BackgroundScheduler

# Import the MonitoringJob model.
#
# The scheduler reads this table to determine
# which monitoring jobs should execute.
from apps.monitoring.models import MonitoringJob

# Import our monitoring service.
#
# This service collects CPU, memory, disk and
# other infrastructure metrics.
from apps.monitoring.services.metric_collector import MetricCollector

# Import the API Monitoring service.
#
# This service checks every registered API endpoint
# and records its health.
from apps.monitoring.services.api_monitor import APIMonitor
# Import the Website Monitoring service.
#
# This service periodically checks the availability
# and response time of websites registered in EIAP.
from apps.monitoring.services.website_monitor import WebsiteMonitor


class SchedulerService:
    """
    Enterprise scheduler service.

    Responsible for configuring and starting
    APScheduler.
    """

    def __init__(self):
        """
        Create a BackgroundScheduler instance.

        This scheduler lives in memory and continuously
        executes registered jobs.
        """

        self.scheduler = BackgroundScheduler()

    def load_monitoring_jobs(self):
        """
        Load monitoring jobs from the database.

        Every enabled MonitoringJob becomes an APScheduler job.
        """

        # Retrieve all enabled monitoring jobs.
        monitoring_jobs = MonitoringJob.objects.filter(
            enabled=True
        )

        print(f"Found {monitoring_jobs.count()} enabled monitoring job(s).")

        # Register each monitoring job.
        for job in monitoring_jobs:

            self.scheduler.add_job(
                # Method executed by APScheduler.
                func=MetricCollector.collect_and_save_metrics,
                # Execute repeatedly.
                trigger="interval",
                # Read the interval from the database.
                seconds=job.interval_seconds,
                # Pass the Server object to the monitoring service.
                args=[job.server],
                # Unique APScheduler job identifier.
                id=f"monitoring_job_{job.id}",
                # Replace existing jobs instead of creating duplicates.
                replace_existing=True,
            )
            # ------------------------------------------------------
            # Schedule API Monitoring.
            # This runs at the same interval as the monitoring job.
            # Every execution:
            # 1. Loads all registered APIs.
            # 2. Performs HTTP health checks.
            # 3. Measures response time.
            # ------------------------------------------------------

            self.scheduler.add_job(
                APIMonitor.monitor_all,
                trigger="interval",
                seconds=job.interval_seconds,
                id=f"api-monitor-{job.id}",
                replace_existing=True,
            )
            # ------------------------------------------------------
            # Schedule Website Monitoring.
            # This job periodically checks every website
            # registered in the system.
            # Workflow
# Scheduler
#      │
#      ▼
# WebsiteMonitor.monitor_all()
#      │
#      ▼
# HTTP Check
#      │
#      ▼
# Update Status
#      │
#      ▼
# Create HealthCheck
            # ------------------------------------------------------

            self.scheduler.add_job(

                # Execute website monitoring.
                WebsiteMonitor.monitor_all,

                # Execute repeatedly.
                trigger="interval",

                # Same interval as the monitoring job.
                seconds=job.interval_seconds,

                # Unique APScheduler job identifier.
                id=f"website-monitor-{job.id}",

                # Prevent duplicate jobs.
                replace_existing=True,
            )

            print(
                f"Loaded monitoring job: "
                f"{job.name} "
                f"({job.interval_seconds}s)"
            )

    def start(self):
        """
        Start the scheduler.

        This method:

        1. Loads jobs from PostgreSQL.
        2. Starts APScheduler.
        """

        self.load_monitoring_jobs()

        self.scheduler.start()

        print("===================================")
        print("EIAP Scheduler Started Successfully")
        print("===================================")

    def shutdown(self):
        """
        Stop the scheduler gracefully.

        Useful during server shutdown.
        """

        self.scheduler.shutdown()
