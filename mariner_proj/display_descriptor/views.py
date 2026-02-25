from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from ..display_descriptor.service import (
    render_display_descriptor,
    DisplayDescriptorService,
)
import json


def _is_descriptor_only(value):
    if value is None:
        return True
    return value.strip().lower() not in {"0", "false", "no", "n", "off"}


@require_GET
def get_display_descriptor(request, resource_id):
    """
    API endpoint to get display descriptor for a resource.

    Usage: GET /api/display-descriptor/<resource_id>/
    """
    try:
        # In a real implementation, you'd fetch the resource data from your models
        # For example:
        # resource = get_resource_data(resource_id)

        # Mock resource data for demonstration
        resource = {
            "Primary Reference Number": "ABC123",
            "Monument Name": [
                {"value": "old church", "Monument Name Use Type": "Primary"},
                {"value": "st mary's church", "Monument Name Use Type": "Statutory"},
                {"value": "church of st mary", "Monument Name Use Type": "Original"},
            ],
        }

        descriptor = render_display_descriptor(resource)

        return JsonResponse(
            {"resource_id": resource_id, "display_descriptor": descriptor}
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def preview_display_descriptor(request):
    """
    API endpoint to preview display descriptor for test data.

    Usage: POST /api/display-descriptor/preview/
    Body: {"resource": {...}, "config": {...}}  (config is optional)

    If config is provided, it will be used for rendering instead of the default config.
    Config can be a dict with keys: "fields" and "display_descriptor_rules"

    Optional query param:
    - descriptor_only=false|0|no|off : returns {"input": {...}, "display_descriptor": "..."}
    - default behavior (or descriptor_only=true) returns only {"display_descriptor": "..."}
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        resource = data.get("resource", {})
        config = data.get("config")
        descriptor_only = _is_descriptor_only(request.GET.get("descriptor_only"))

        # Use provided config or fall back to default
        if config:
            try:
                service = DisplayDescriptorService()
                descriptor = service.render_with_config(resource, config)
            except ValueError as e:
                return JsonResponse({"error": f"Invalid config: {str(e)}"}, status=400)
        else:
            descriptor = render_display_descriptor(resource)

        if descriptor_only:
            return JsonResponse({"display_descriptor": descriptor})

        return JsonResponse({"input": resource, "display_descriptor": descriptor})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
