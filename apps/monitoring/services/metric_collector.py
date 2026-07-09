"""
Metric Collection Service

This module is responsible for collecting infrastructure
metrics from monitored resources.

Initially, it collects metrics from the local machine using
the psutil library.

Later this service will also support:

- Remote Servers
- REST APIs
- Websites
- Databases
- Docker Containers

Author:
Enterprise Infrastructure & Automation Platform (EIAP)
"""

import psutil
from apps.monitoring.models import Metric
from apps.monitoring.models import Server


class MetricCollector:
    """
    Service responsible for collecting system metrics.

    This class hides the implementation details of metric
    collection from the rest of the application.

    Other parts of the system only need to call:

        MetricCollector.collect_local_metrics()

    They don't need to know how the values are collected.
    """

    @staticmethod
    def collect_local_metrics():
        """
        Collect CPU, memory and disk usage from
        the local machine.

        Returns
        -------
        dict
            Dictionary containing collected metrics.

        Example
        -------
        {
            "cpu_usage": 21.5,
            "memory_usage": 48.3,
            "disk_usage": 61.2,
        }
        """

        # --------------------------------------------------
        # Current CPU utilization percentage.
        # interval=1 measures usage over one second.
        # --------------------------------------------------
        cpu_usage = psutil.cpu_percent(interval=1)

        # --------------------------------------------------
        # Current memory utilization percentage.
        # --------------------------------------------------
        memory_usage = psutil.virtual_memory().percent

        # --------------------------------------------------
        # Current disk utilization percentage.
        #
        # On Windows, "/" automatically refers to the
        # current drive. Later we'll make this configurable.
        # --------------------------------------------------
        disk_usage = psutil.disk_usage("/").percent

        # Return all collected values.
        return {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage,
        }

    @staticmethod
    def collect_and_save_metrics(server: Server) -> Metric:
        """
        Collect metrics from the local machine and save them
        to the database.

        Parameters
        ----------
        server : Server
            The monitored server/resource these metrics belong to.

        Returns
        -------
        Metric
            The newly created Metric database record.
        """

        # First, collect the latest system metrics.
        metrics = MetricCollector.collect_local_metrics()

        # Create and save a new Metric record.
        metric = Metric.objects.create(
            server=server,
            cpu_usage=metrics["cpu_usage"],
            memory_usage=metrics["memory_usage"],
            disk_usage=metrics["disk_usage"],
            status="Healthy",
        )

        return metric
