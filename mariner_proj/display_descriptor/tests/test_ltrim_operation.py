from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_ltrim


class LTrimOperationTests(SimpleTestCase):
    def test_ltrim(self):
        self.assertEqual(op_ltrim("  hello  "), "hello  ")
