from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_normalize_whitespace


class NormalizeWhitespaceOperationTests(SimpleTestCase):
    def test_normalize_whitespace(self):
        self.assertEqual(
            op_normalize_whitespace("  old\n\tchurch   name "),
            "old church name",
        )
