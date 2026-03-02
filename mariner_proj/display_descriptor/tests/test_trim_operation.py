from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_trim


class TrimOperationTests(SimpleTestCase):
    def test_trim(self):
        self.assertEqual(op_trim("  hello  "), "hello")
