from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import (
    apply_operation_chain,
    op_rpad,
)
from mariner_proj.display_descriptor.models import Operation


class RPadOperationTests(SimpleTestCase):
    def test_rpad(self):
        self.assertEqual(op_rpad("42", pad_length=4, pad_char="."), "42..")

    def test_rpad_in_operation_chain(self):
        value = apply_operation_chain(
            "42", [Operation(type="rpad", pad_length=5, pad_char=".")]
        )
        self.assertEqual(value, "42...")
