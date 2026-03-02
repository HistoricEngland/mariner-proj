from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_remove_diacritics


class RemoveDiacriticsOperationTests(SimpleTestCase):
    def test_remove_diacritics(self):
        self.assertEqual(op_remove_diacritics("Château"), "Chateau")
