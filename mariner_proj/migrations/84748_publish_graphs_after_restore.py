from django.db import migrations
from django.utils import translation
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from arches.app.models.system_settings import settings
from arches.app.models.resource import UnpublishedModelError
from arches.app.models.graph import Graph
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
import uuid
import datetime

import logging

logger = logging.getLogger(__name__)


def publish_graphs_after_restore(apps, schema_editor):
    """
    Publish all graphs after restore
    """
    try:
        system_user = User.objects.get(username="admin")
    except User.DoesNotExist:
        # Fall back to any superuser if 'admin' does not exist
        system_user = User.objects.filter(is_superuser=True).first()
        if not system_user:
            raise Exception("No superuser found to publish graphs.")

    graphs_to_publish = Graph.objects.filter(
        isresource=True, publication__isnull=True
    )

    for graph in graphs_to_publish:
        try:
            graph.publish(
                user=system_user,
                notes=_("Published after restore"),
            )
        except Exception as e:
            logger.error(f"Failed to publish graph {graph.graphid}: {e}")
            raise UnpublishedModelError(e)


class Migration(migrations.Migration):

    initial = False

    dependencies = [
        ("mariner_app", "84748_initial_bng_photo_datatype_functions_widgets"),
        ("mariner_proj", "84748_mariner_restore_steps"),
    ]

    operations = [
        migrations.RunPython(publish_graphs_after_restore),
    ]
