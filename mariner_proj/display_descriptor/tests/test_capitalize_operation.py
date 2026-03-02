from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_capitalize


class CapitalizeOperationTests(SimpleTestCase):
    def test_capitalize_on_string(self):
        self.assertEqual(op_capitalize("sT MARY"), "St mary")
