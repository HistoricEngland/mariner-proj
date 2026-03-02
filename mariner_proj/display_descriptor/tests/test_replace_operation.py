from django.test import SimpleTestCase

from mariner_proj.display_descriptor.display_descriptor import (
    apply_operation_chain,
    op_replace,
)
from mariner_proj.display_descriptor.models import Operation


class ReplaceOperationTests(SimpleTestCase):
    def test_op_replace_is_case_sensitive_by_default(self):
        value = "church of st mary"

        result = op_replace(value, replace_from="Church Of", replace_to="Church of")

        self.assertEqual(result, "church of st mary")

    def test_op_replace_supports_ignore_case(self):
        value = "church of st mary"

        result = op_replace(
            value,
            replace_from="Church Of",
            replace_to="Church of",
            ignore_case=True,
        )

        self.assertEqual(result, "Church of st mary")

    def test_apply_operation_chain_replace_ignore_case(self):
        value = "church of st mary"
        operations = [
            Operation(
                type="replace",
                replace_from="Church Of",
                replace_to="Church of",
                ignore_case=True,
            )
        ]

        result = apply_operation_chain(value, operations)

        self.assertEqual(result, "Church of st mary")
