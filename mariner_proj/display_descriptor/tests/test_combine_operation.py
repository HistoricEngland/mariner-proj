from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_combine


class CombineOperationTests(SimpleTestCase):
    def test_combine_with_max_items_and_dicts(self):
        values = ["Church", {"value": "Abbey"}, "Priory"]
        self.assertEqual(
            op_combine(values, separator=" | ", max_items=2), "Church | Abbey"
        )

    def test_combine_with_max_length(self):
        values = ["Church", {"value": "Abbey"}, "Priory"]
        self.assertEqual(
            op_combine(values, separator=", ", max_length=8, overflow_indicator="..."),
            "Church, ...",
        )
