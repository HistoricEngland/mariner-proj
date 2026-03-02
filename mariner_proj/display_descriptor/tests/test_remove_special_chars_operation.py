from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_remove_special_chars


class RemoveSpecialCharsOperationTests(SimpleTestCase):
    def test_remove_special_chars(self):
        self.assertEqual(
            op_remove_special_chars("St. Mary's (Church)!"), "St Marys Church"
        )
