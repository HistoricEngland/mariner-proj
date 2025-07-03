import sys
from uuid import UUID

from django.db import DatabaseError, IntegrityError, migrations


def load_spatialviews(apps, schema_editor):
    try:
        SpatialView = apps.get_model("models", "SpatialView")
    except LookupError as e:
        print(
            f"Warning: Could not get SpatialView model: {e}. Skipping spatialview migration (likely running in test or incomplete DB setup)."
        )
        return
    records = [
        {
            "spatialviewid": UUID("a15ac9f1-3b8b-4c30-9872-0a5a9a89b2e8"),
            "schema": "public",
            "slug": "activity",
            "description": "Used to record events relating to a particular Heritage Resource. Activities can be used to give context and meaning to the records of heritage assets. They provide information on ‘how we know what we know’ (for example investigative activities or research and analysis) or on how a particular Heritage Asset has been managed through time (management activities). Last updated: January 2024",
            "ismixedgeometrytypes": False,
            "attributenodes": [
                {
                    "nodeid": "4a7be135-9938-11ea-b0e2-f875a44e0e11",
                    "description": "activity_name",
                },
                {
                    "nodeid": "44441e0c-99ac-11ea-97cc-f875a44e0e11",
                    "description": "primary_reference_number",
                },
            ],
            "isactive": True,
            "geometrynode_id": UUID("b2b381e5-1459-11eb-ab26-f875a44e0e11"),
            "language_id": "en",
        },
        {
            "spatialviewid": UUID("747a8dd6-70e3-47f7-ac6b-e704f8ea1a43"),
            "schema": "public",
            "slug": "aircraft_crash_site",
            "description": "Used to record the remains of structures and artefact assemblages associated with the wreck of a vessel or aircraft. Last updated: January 2024",
            "ismixedgeometrytypes": False,
            "attributenodes": [
                {
                    "nodeid": "190f65cc-33ae-11ef-8f99-0242ac120006",
                    "description": "crash_site_name",
                },
                {
                    "nodeid": "190e1a1e-33ae-11ef-8f99-0242ac120006",
                    "description": "primary_reference_number",
                },
            ],
            "isactive": True,
            "geometrynode_id": UUID("190f34a8-33ae-11ef-8f99-0242ac120006"),
            "language_id": "en",
        },
        {
            "spatialviewid": UUID("7bfe40d2-0faa-427b-b565-87a46cc05d27"),
            "schema": "public",
            "slug": "climate_hazard",
            "description": "",
            "ismixedgeometrytypes": False,
            "attributenodes": [
                {
                    "nodeid": "5477031c-11f9-11ef-9565-0242ac120006",
                    "description": "name",
                },
                {
                    "nodeid": "9a1c8f00-145f-11ef-b089-0242ac130006",
                    "description": "primary_reference_number",
                },
            ],
            "isactive": True,
            "geometrynode_id": UUID("55d522aa-144e-11ef-9fc8-0242ac130006"),
            "language_id": "en",
        },
        {
            "spatialviewid": UUID("011d068a-14db-41f4-b9cb-b2a3ed56995c"),
            "schema": "public",
            "slug": "coastal_peat_site",
            "description": "Used to record details of coastal and intertidal sites from which peat samples have been  extracted. Based on the data model from the Historic England Coastal and Intertidal Peat Database. Last updated January 2024",
            "ismixedgeometrytypes": False,
            "attributenodes": [
                {
                    "nodeid": "f0f95950-a937-11ed-b890-0242ac130006",
                    "description": "site_name",
                },
                {
                    "nodeid": "b2b30a04-ad1c-11ed-acf1-0242ac130006",
                    "description": "primary_reference_number",
                },
            ],
            "isactive": True,
            "geometrynode_id": UUID("3a047c7c-ad1d-11ed-af5b-0242ac130006"),
            "language_id": "en",
        },
        {
            "spatialviewid": UUID("36a16183-67f9-40dd-863a-770cbfaed5ac"),
            "schema": "public",
            "slug": "heritage_story",
            "description": "Used to record  thematic stories (usually associated with an historic event or period) which can provide more detailed background to the heritage assets, areas and artefact. The Heritage Story creates a user-friendly story which helps place the assets in their context within the historic environment. Last updated: January 2024.",
            "ismixedgeometrytypes": False,
            "attributenodes": [
                {
                    "nodeid": "4bc44105-99aa-11ea-aaa3-f875a44e0e11",
                    "description": "name",
                },
                {
                    "nodeid": "44441e0c-99ac-11ea-97cc-f875a44e0e11",
                    "description": "primary_reference_number",
                },
            ],
            "isactive": True,
            "geometrynode_id": UUID("38521798-3bd0-11eb-ad57-f875a44e0e11"),
            "language_id": "en",
        },
        {
            "spatialviewid": UUID("5dc4eb00-3cdd-433f-bec6-17bf3975797a"),
            "schema": "public",
            "slug": "historic_aircraft",
            "description": "Used to record the details of historic aircraft which are either retained as heritage assets (eg. Museum exhibits or Gate Guardians) or have been identified through the discovery of associated crash sites. A Wreck Site or Monument record should be created for the crash site where known. Last Updated January 2024",
            "ismixedgeometrytypes": False,
            "attributenodes": [
                {
                    "nodeid": "008e66d1-28e0-11eb-b03a-f875a44e0e11",
                    "description": "name",
                },
                {
                    "nodeid": "95495b17-298b-11eb-b6cb-f875a44e0e11",
                    "description": "primary_reference_number",
                },
            ],
            "isactive": True,
            "geometrynode_id": UUID("30f52d8a-3e07-11eb-9a63-f875a44e0e11"),
            "language_id": "en",
        },
        {
            "spatialviewid": UUID("25481123-f14e-4f83-bad0-08b0c24bdda8"),
            "schema": "public",
            "slug": "historic_event",
            "description": "",
            "ismixedgeometrytypes": False,
            "attributenodes": [
                {
                    "nodeid": "10a8d52a-1848-11ef-9bf8-0242ac130006",
                    "description": "name",
                },
                {
                    "nodeid": "a9fa7f04-1851-11ef-88ae-0242ac130006",
                    "description": "primary_reference_number",
                },
            ],
            "isactive": True,
            "geometrynode_id": UUID("a93c8c00-1848-11ef-b394-0242ac130006"),
            "language_id": "en",
        },
        {
            "spatialviewid": UUID("51f17799-590a-4ab5-804a-e31d164f120a"),
            "schema": "public",
            "slug": "maritime_vessel",
            "description": "Used to record the details of historic vessels which are either retained as heritage assets (eg. Museum Ships or Memorials) or have been identified through the discovery of associated wreck sites. A Heritage Asset record should be created for the wreck site where known. Last updated: January 2024.",
            "ismixedgeometrytypes": False,
            "attributenodes": [
                {
                    "nodeid": "d00d4c8c-299f-11eb-bc0e-f875a44e0e11",
                    "description": "name",
                },
                {
                    "nodeid": "95495b17-298b-11eb-b6cb-f875a44e0e11",
                    "description": "primary_reference_number",
                },
            ],
            "isactive": True,
            "geometrynode_id": UUID("ce5aad62-3e0e-11eb-b8d2-f875a44e0e11"),
            "language_id": "en",
        },
        {
            "spatialviewid": UUID("2c9dca15-168a-41c6-9cfa-58ae2f02d042"),
            "schema": "public",
            "slug": "monument",
            "description": "Used to record built works, human-made structures and human-modified features. These can range from a single post box to a palace complex. The use of Monument or Site will be a question of granularity. Last updated: January 2024.",
            "ismixedgeometrytypes": False,
            "attributenodes": [
                {
                    "nodeid": "676d47ff-9c1c-11ea-b07f-f875a44e0e11",
                    "description": "monument_name",
                },
                {
                    "nodeid": "2182c97e-b532-11ee-b6dc-0242ac120006",
                    "description": "primary_reference_number",
                },
            ],
            "isactive": True,
            "geometrynode_id": UUID("ca063178-28cf-11eb-be6d-f875a44e0e11"),
            "language_id": "en",
        },
        {
            "spatialviewid": UUID("40fa4acf-ef6c-4c56-9f7a-c129a4cbc644"),
            "schema": "public",
            "slug": "period",
            "description": "Used to record the details of historic and cultural periods which a heritage resource may be associated with. \nA period is a spatio-temporal extent so where you are influences the period.",
            "ismixedgeometrytypes": False,
            "attributenodes": [
                {
                    "nodeid": "2ce82688-8862-11ea-86b9-f875a44e0e11",
                    "description": "period_name",
                },
                {
                    "nodeid": "2501f374-9458-11ea-b75f-f875a44e0e11",
                    "description": "primary_reference_number",
                },
            ],
            "isactive": True,
            "geometrynode_id": UUID("3e42372e-3edf-11eb-bf20-f875a44e0e11"),
            "language_id": "en",
        },
        {
            "spatialviewid": UUID("1dcf6c0d-df52-4456-ae31-fc802af0b435"),
            "schema": "public",
            "slug": "place",
            "description": "Used to record places as spatio-temporal resources. Last updated: January 2024",
            "ismixedgeometrytypes": False,
            "attributenodes": [
                {
                    "nodeid": "972d3869-b6f2-11ea-8f39-f875a44e0e11",
                    "description": "placename",
                },
                {
                    "nodeid": "d6772ed4-b6da-11ee-9b93-0242ac120006",
                    "description": "primary_reference_number",
                },
            ],
            "isactive": True,
            "geometrynode_id": UUID("cb6cf3e7-4f66-11eb-bd0a-f875a44e0e11"),
            "language_id": "en",
        },
        {
            "spatialviewid": UUID("4cd30b8f-2f2d-4e1c-98dc-f3089051d36e"),
            "schema": "public",
            "slug": "seascape_characterization",
            "description": "Used to record areas of the historic landscape. Seascape Characterization is a method of identifying and interpreting the varying character within an area that looks beyond individual heritage assets as it brings together an understanding of the whole seascape Last updated: January 2024.",
            "ismixedgeometrytypes": False,
            "attributenodes": [
                {
                    "nodeid": "4cf307e2-07b5-11eb-8253-f875a44e0e11",
                    "description": "name",
                },
                {
                    "nodeid": "99456f68-0dfd-11eb-b132-f875a44e0e11",
                    "description": "primary_reference_number",
                },
            ],
            "isactive": True,
            "geometrynode_id": UUID("6678040f-3dff-11eb-a042-f875a44e0e11"),
            "language_id": "en",
        },
        {
            "spatialviewid": UUID("69a3eae6-e45c-4596-845a-87014a06d777"),
            "schema": "public",
            "slug": "site",
            "description": "Used to record complex human-made, or human conceived, sites, areas or landscapes. Sites can be anything from a simple prehistoric settlement site (evidenced by a few flint-working fragments) to large-scale, urban conservation areas incorporating multiple assets within a city. The use of Site or Monument will be a question of granularity.\n\nFor building complexes such as castles, prisons and airfields, Site may be used to record the footprint of the site, eg. the curtain wall and outer defences of a castle. This Site can then be used as the parent for multiple Monument records. Last updated: January 2024.",
            "ismixedgeometrytypes": False,
            "attributenodes": [
                {
                    "nodeid": "f45dbbe8-80b7-11ea-b325-f875a44e0e11",
                    "description": "site_name",
                },
                {
                    "nodeid": "e0ffa302-b551-11ee-92d8-0242ac120006",
                    "description": "primary_reference_number",
                },
            ],
            "isactive": True,
            "geometrynode_id": UUID("64be56e3-3ee5-11eb-b1f0-f875a44e0e11"),
            "language_id": "en",
        },
        {
            "spatialviewid": UUID("c5f9fc90-fe2f-486b-a2b8-66815ffc6c75"),
            "schema": "public",
            "slug": "wreck_site",
            "description": "Used to record the remains of structures and artefact assemblages associated with the wreck of a vessel or aircraft. Last updated: January 2024",
            "ismixedgeometrytypes": False,
            "attributenodes": [
                {
                    "nodeid": "e14eef30-ee59-11ed-94d5-0242ac120006",
                    "description": "wreck_site_name",
                },
                {
                    "nodeid": "e14c9ca8-ee59-11ed-94d5-0242ac120006",
                    "description": "primary_reference_number",
                },
            ],
            "isactive": True,
            "geometrynode_id": UUID("e14cdbd2-ee59-11ed-94d5-0242ac120006"),
            "language_id": "en",
        },
    ]

    # Check for geometrynode existence before inserting
    Node = None
    try:
        Node = apps.get_model("models", "Node")
    except LookupError:
        print(
            "Warning: Could not get Node model. Skipping geometrynode existence checks.",
            file=sys.stderr,
        )

    for record in records:
        geometrynode_id = record.get("geometrynode_id")
        if Node is not None and geometrynode_id is not None:
            if not Node.objects.filter(nodeid=geometrynode_id).exists():
                print(
                    f"[DEBUG] Skipping SpatialView '{record['slug']}' because geometrynode_id {geometrynode_id} does not exist in nodes table.",
                    file=sys.stderr,
                )
                continue
        try:
            SpatialView.objects.update_or_create(
                spatialviewid=record["spatialviewid"], defaults=record
            )
        except (IntegrityError, DatabaseError, Exception) as e:
            # Log a debug warning, but do not fail the migration if the data is missing (e.g., during testing)
            print(
                f"[DEBUG] Could not insert or update SpatialView {record['slug']}: {e}",
                file=sys.stderr,
            )
            continue


def unload_spatialviews(apps, schema_editor):
    try:
        SpatialView = apps.get_model("models", "SpatialView")
    except LookupError as e:
        import sys

        print(
            f"[DEBUG] Could not get SpatialView model: {e}. Skipping spatialview unload (likely running in test or incomplete DB setup).",
            file=sys.stderr,
        )
        return
    spatialviewids = [
        UUID("a15ac9f1-3b8b-4c30-9872-0a5a9a89b2e8"),
        UUID("747a8dd6-70e3-47f7-ac6b-e704f8ea1a43"),
        UUID("7bfe40d2-0faa-427b-b565-87a46cc05d27"),
        UUID("011d068a-14db-41f4-b9cb-b2a3ed56995c"),
        UUID("36a16183-67f9-40dd-863a-770cbfaed5ac"),
        UUID("5dc4eb00-3cdd-433f-bec6-17bf3975797a"),
        UUID("25481123-f14e-4f83-bad0-08b0c24bdda8"),
        UUID("51f17799-590a-4ab5-804a-e31d164f120a"),
        UUID("2c9dca15-168a-41c6-9cfa-58ae2f02d042"),
        UUID("40fa4acf-ef6c-4c56-9f7a-c129a4cbc644"),
        UUID("1dcf6c0d-df52-4456-ae31-fc802af0b435"),
        UUID("4cd30b8f-2f2d-4e1c-98dc-f3089051d36e"),
        UUID("69a3eae6-e45c-4596-845a-87014a06d777"),
        UUID("c5f9fc90-fe2f-486b-a2b8-66815ffc6c75"),
    ]
    SpatialView.objects.filter(spatialviewid__in=spatialviewids).delete()


class Migration(migrations.Migration):
    dependencies = [("mariner_proj", "84748_publish_graphs_after_restore")]

    operations = [
        migrations.RunPython(load_spatialviews, reverse_code=unload_spatialviews),
    ]
