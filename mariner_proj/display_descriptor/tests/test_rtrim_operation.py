from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_rtrim


class RTrimOperationTests(SimpleTestCase):
    def test_rtrim(self):
        self.assertEqual(op_rtrim("  hello  "), "  hello")
