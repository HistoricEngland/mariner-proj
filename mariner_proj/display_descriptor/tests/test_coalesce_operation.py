from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_coalesce


class CoalesceOperationTests(SimpleTestCase):
    def test_coalesce_none_and_blank(self):
        self.assertEqual(op_coalesce(None, coalesce_value="Unknown"), "Unknown")
        self.assertEqual(op_coalesce("   ", coalesce_value="Unknown"), "Unknown")

    def test_coalesce_empty_list(self):
        self.assertEqual(op_coalesce([], coalesce_value="Unknown"), "Unknown")

    def test_coalesce_list_items(self):
        self.assertEqual(
            op_coalesce(["", "abc", None], coalesce_value="Unknown"),
            ["Unknown", "abc", "Unknown"],
        )
