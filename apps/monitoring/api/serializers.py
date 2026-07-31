"""
Monitoring API Serializers

Serializers convert Django model instances into JSON
and convert incoming JSON into Django model instances.

Think of a serializer as a translator between:

Django Models  <------->  JSON

Every model exposed through the REST API should have
its own serializer.
"""

# Django REST Framework serializer classes.
from rest_framework import serializers

# Import the model that will be exposed through the API.
from apps.monitoring.models import Server


class ServerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Server model.

    ModelSerializer automatically generates serializer
    fields based on the Django model.

    This serializer will be used for:

    • Listing servers
    • Retrieving a single server
    • Creating servers
    • Updating servers
    • Deleting servers
    """

    class Meta:
        """
        Serializer configuration.
        """

        #
        # Model that this serializer represents.
        #
        model = Server

        #
        # Include every model field.
        #
        fields = "__all__"
