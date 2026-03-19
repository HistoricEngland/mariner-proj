from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mariner_proj", "84212_mariner_initial_spatialviews"),
    ]

    operations = [
        migrations.CreateModel(
            name="DisplayDescriptorGraphConfig",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("graph_id", models.UUIDField(db_index=True, unique=True)),
                ("yaml_config", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "display_descriptor_graph_config",
                "verbose_name": "Display descriptor graph config",
                "verbose_name_plural": "Display descriptor graph configs",
            },
        ),
    ]
