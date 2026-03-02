from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_uppercase


class UppercaseOperationTests(SimpleTestCase):
    def test_uppercase_on_string(self):
        self.assertEqual(op_uppercase("Abc"), "ABC")
