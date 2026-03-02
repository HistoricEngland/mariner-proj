from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import apply_operation_chain
from mariner_proj.display_descriptor.models import Operation


class ApplyOperationChainBehaviorTests(SimpleTestCase):
    def test_unknown_operation_raises(self):
        with self.assertRaisesRegex(ValueError, "Unknown operation type"):
            apply_operation_chain("value", [Operation(type="not_real")])

    def test_multiple_handlers_chain(self):
        result = apply_operation_chain(
            "42",
            [
                Operation(type="lpad", pad_length=4, pad_char="0"),
                Operation(type="rpad", pad_length=5, pad_char="."),
            ],
        )
        self.assertEqual(result, "0042.")
