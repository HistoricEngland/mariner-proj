from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import op_reverse


class ReverseOperationTests(SimpleTestCase):
    def test_reverse_list(self):
        self.assertEqual(op_reverse([1, 2, 3]), [3, 2, 1])

    def test_reverse_no_effect_on_string(self):
        self.assertEqual(op_reverse("abc"), "abc")
