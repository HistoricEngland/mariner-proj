from django.db import migrations
from django.utils import translation
from django.utils.translation import gettext as _
from arches.app.models.system_settings import settings
from arches.app.models.resource import UnpublishedModelError
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
import uuid
import datetime


def publish_proxy(apps, graph, user, notes=None):
    """
    Proxy the code for arches.app.models.Graph.publish() at 7.6.x

    `apps.get_model` only provides the historical model without
    the instance code.

    """
    self = graph

    GraphXPublishedGraph = apps.get_model("models", "GraphXPublishedGraph")
    Language = apps.get_model("models", "Language")
    PublishedGraph = apps.get_model("models", "PublishedGraph")

    try:
        publication = GraphXPublishedGraph.objects.create(
            graph=self,
            notes=notes,
            user=user,
        )
        publication.save()

        self.publication = publication
        self.save()

        for language_tuple in settings.LANGUAGES:
            language = Language.objects.get(code=language_tuple[0])

            translation.activate(language=language_tuple[0])

            published_graph = PublishedGraph.objects.create(
                publication=publication,
                serialized_graph=JSONDeserializer().deserialize(
                    JSONSerializer().serialize(self, force_recalculation=True)
                ),
                language=language,
            )

            published_graph.save()

        translation.deactivate()
    except Exception as e:
        print(f"Error publishing graph {self.name}:", e)
        raise UnpublishedModelError(e)


def publish_graphs_after_restore(apps, schema_editor):
    """
    Publish all graphs after restore
    """
    system_settings_id = settings.SYSTEM_SETTINGS_RESOURCE_MODEL_ID
    Graph = apps.get_model("models", "GraphModel")

    # Use the admin user for the publication process
    User = apps.get_model("auth", "User")
    try:
        system_user = User.objects.get(username="admin")
    except User.DoesNotExist:
        # Fall back to any superuser if 'admin' does not exist
        system_user = User.objects.filter(is_superuser=True).first()
        if not system_user:
            raise Exception("No superuser found to publish graphs.")

    # Get all unpublished resource graphs excluding the system settings model
    graphs_to_publish = Graph.objects.filter(
        isresource=True, publication__isnull=True
    ).exclude(graphid=system_settings_id)

    # Publish each graph using proxy function
    for graph in graphs_to_publish:
        publish_proxy(apps, graph, system_user, notes=_("Published after restore"))


class Migration(migrations.Migration):

    initial = False

    dependencies = [
        ("mariner_app", "84748_initial_bng_photo_datatype_functions_widgets"),
        ("mariner_proj", "84748_mariner_restore_steps"),
    ]

    operations = [
        migrations.RunPython(publish_graphs_after_restore),
    ]
