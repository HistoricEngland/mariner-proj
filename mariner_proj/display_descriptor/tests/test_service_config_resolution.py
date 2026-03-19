from unittest.mock import patch

from django.test import SimpleTestCase

from mariner_proj.display_descriptor.models import DisplayDescriptorConfig
from mariner_proj.display_descriptor.service import DisplayDescriptorService


class DisplayDescriptorServiceConfigResolutionTests(SimpleTestCase):
    def test_resolve_config_prefers_api_override(self):
        service = DisplayDescriptorService()
        override = {"fields": [], "display_descriptor_rules": []}

        with (
            patch.object(service, "_get_resource_graph_id") as mock_graph,
            patch.object(service, "_load_graph_config") as mock_graph_config,
        ):
            resolved = service._resolve_config("resource-id", config_data=override)

        self.assertIsInstance(resolved, DisplayDescriptorConfig)
        mock_graph.assert_not_called()
        mock_graph_config.assert_not_called()

    def test_resolve_config_uses_graph_lookup_without_override(self):
        service = DisplayDescriptorService()
        db_config = DisplayDescriptorConfig(fields=[], display_descriptor_rules=[])

        with (
            patch.object(
                service, "_get_resource_graph_id", return_value="graph-id"
            ) as mock_graph,
            patch.object(
                service, "_load_graph_config", return_value=db_config
            ) as mock_graph_config,
        ):
            resolved = service._resolve_config("resource-id", config_data=None)

        self.assertEqual(resolved, db_config)
        mock_graph.assert_called_once_with("resource-id")
        mock_graph_config.assert_called_once_with("graph-id")

    def test_render_for_resource_returns_none_when_no_config(self):
        service = DisplayDescriptorService()

        with patch.object(service, "get_resource_data", return_value=({}, None)):
            descriptor = service.render_for_resource("resource-id")

        self.assertIsNone(descriptor)

    def test_render_without_explicit_config_is_noop(self):
        service = DisplayDescriptorService()

        descriptor = service.render({"Primary Reference Number": "123"})

        self.assertIsNone(descriptor)

    def test_load_config_from_yaml_requires_object(self):
        service = DisplayDescriptorService()

        with self.assertRaises(ValueError):
            service.load_config_from_yaml("- one\n- two\n")
