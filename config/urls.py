"""
Project URL Configuration

This module defines the root URL routes for the
Enterprise Infrastructure Automation Platform (EIAP).

Each application is responsible for maintaining its
own URLs. The project simply includes them here.
"""

# Django admin site.
from django.contrib import admin

# URL routing utilities.
from django.urls import (
    include,
    path,
)

# ==========================================================
# Root URL Configuration
# ==========================================================

urlpatterns = [

    #
    # Django Administration.
    #
    path(
        "admin/",
        admin.site.urls,
    ),

    #
    # Monitoring REST API.
    #
    path(
        "api/",
        include(
            "apps.monitoring.api.urls",
        ),
    ),
    #
    # Browser Automation APIs.
    #
    path(
        "api/",
        include(
            "apps.browser.api.urls",
        ),
    ),


]
