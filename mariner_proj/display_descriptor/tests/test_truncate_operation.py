from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_truncate


class TruncateOperationTests(SimpleTestCase):
    def test_truncate_with_indicator(self):
        self.assertEqual(
            op_truncate("abcdefghij", max_length=7, truncate_indicator="..."), "abcd..."
        )

    def test_truncate_indicator_longer_than_max(self):
        self.assertEqual(
            op_truncate("abc", max_length=2, truncate_indicator="....."), ".."
        )
