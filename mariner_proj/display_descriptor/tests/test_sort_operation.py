from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_sort


class SortOperationTests(SimpleTestCase):
    def test_sort_handles_strings_and_dict_values(self):
        values = ["zebra", {"value": "Apple"}, "cherry"]
        self.assertEqual(op_sort(values), [{"value": "Apple"}, "cherry", "zebra"])
