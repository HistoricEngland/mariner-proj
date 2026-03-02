from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import (
    apply_operation_chain,
    op_lpad,
)
from mariner_proj.display_descriptor.models import Operation


class LPadOperationTests(SimpleTestCase):
    def test_lpad(self):
        self.assertEqual(op_lpad("42", pad_length=4, pad_char="0"), "0042")

    def test_lpad_no_effect_if_shorter_target(self):
        self.assertEqual(op_lpad("abcd", pad_length=3, pad_char="0"), "abcd")

    def test_lpad_in_operation_chain(self):
        value = apply_operation_chain(
            "42", [Operation(type="lpad", pad_length=4, pad_char="0")]
        )
        self.assertEqual(value, "0042")
