from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_prefix


class PrefixOperationTests(SimpleTestCase):
    def test_prefix_string(self):
        self.assertEqual(op_prefix("Church", prefix_value="[SITE] "), "[SITE] Church")
