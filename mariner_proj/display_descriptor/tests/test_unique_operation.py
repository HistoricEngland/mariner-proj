from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_unique


class UniqueOperationTests(SimpleTestCase):
    def test_unique_preserves_order_and_handles_dict_items(self):
        values = ["Church", "Church", {"value": "Abbey"}, {"value": "Abbey"}, "Priory"]
        self.assertEqual(op_unique(values), ["Church", {"value": "Abbey"}, "Priory"])
