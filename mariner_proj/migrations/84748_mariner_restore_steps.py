"""
DROP SCHEMA IF EXISTS activity CASCADE;
DROP SCHEMA IF EXISTS aircraft_crash_site CASCADE;
DROP SCHEMA IF EXISTS artefact CASCADE;
DROP SCHEMA IF EXISTS bibliographic_source CASCADE;
DROP SCHEMA IF EXISTS historic_aircraft CASCADE;
DROP SCHEMA IF EXISTS maritime_vessel CASCADE;
DROP SCHEMA IF EXISTS monument CASCADE;
DROP SCHEMA IF EXISTS organization CASCADE;
DROP SCHEMA IF EXISTS period CASCADE;
DROP SCHEMA IF EXISTS person CASCADE;
DROP SCHEMA IF EXISTS place CASCADE;
DROP SCHEMA IF EXISTS wreck_site CASCADE;
"""

from django.db import migrations
from django.utils.translation import gettext as _
from arches.app.models.system_settings import settings
from django.contrib.auth.models import User


class Migration(migrations.Migration):

    initial = True

    run_before = [
        ("models", "6458_language"),
    ]

    def fix_data_after_restore(apps, schema_editor):
        """
        Fix data after restore
        """
        # Update languageid to 'en-us'
        Value = apps.get_model("models", "Value")
        Value.objects.filter(language_id="en-US").update(language_id="en-us")

        # Drop schemas if they exist
        schemas_to_drop = [
            "activity",
            "aircraft_crash_site",
            "artefact",
            "bibliographic_source",
            "historic_aircraft",
            "maritime_vessel",
            "monument",
            "organization",
            "period",
            "person",
            "place",
            "wreck_site",
        ]
        for schema in schemas_to_drop:
            schema_editor.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE")

    operations = [
        migrations.RunPython(fix_data_after_restore),
    ]
