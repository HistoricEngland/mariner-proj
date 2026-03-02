from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import apply_operation_chain
from mariner_proj.display_descriptor.models import Operation


class FallbackTextOperationTests(SimpleTestCase):
    def test_fallback_text_alias(self):
        value = apply_operation_chain(
            None, [Operation(type="fallback_text", fallback_text="Unknown")]
        )
        self.assertEqual(value, "Unknown")
