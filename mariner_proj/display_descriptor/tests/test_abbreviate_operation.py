from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_abbreviate


class AbbreviateOperationTests(SimpleTestCase):
    def test_abbreviate_with_skip_words(self):
        self.assertEqual(
            op_abbreviate("Church Of Saint Mary", skip_words=["of"]), "CSM"
        )

    def test_abbreviate_with_length_and_lowercase(self):
        self.assertEqual(
            op_abbreviate(
                "Church Of Saint Mary",
                length_per_word=2,
                skip_words=["of"],
                uppercase=False,
            ),
            "ChSaMa",
        )
