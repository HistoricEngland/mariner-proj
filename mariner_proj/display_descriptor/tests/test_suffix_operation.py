from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_suffix


class SuffixOperationTests(SimpleTestCase):
    def test_suffix_list(self):
        self.assertEqual(
            op_suffix(["Church", "Abbey"], suffix_value=" Listed"),
            ["Church Listed", "Abbey Listed"],
        )
