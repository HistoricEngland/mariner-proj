from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_titlecase


class TitlecaseOperationTests(SimpleTestCase):
    def test_titlecase_on_string(self):
        self.assertEqual(op_titlecase("st mary's CHURCH"), "St Mary's Church")

    def test_titlecase_on_list(self):
        self.assertEqual(
            op_titlecase(["old church", "st mary"]),
            ["Old Church", "St Mary"],
        )
