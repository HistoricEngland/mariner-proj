from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_lowercase


class LowercaseOperationTests(SimpleTestCase):
    def test_lowercase_on_string(self):
        self.assertEqual(op_lowercase("AbC"), "abc")
