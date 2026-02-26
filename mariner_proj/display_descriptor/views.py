from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.conf import settings
from ..display_descriptor.service import (
    render_display_descriptor,
    render_display_descriptor_for_resource,
    DisplayDescriptorService,
)
import json
from time import perf_counter


def _is_descriptor_only(value):
    if value is None:
        return True
    return value.strip().lower() not in {"0", "false", "no", "n", "off"}


def _is_truthy(value):
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _execute_with_sql_capture(func, include_sql=False):
    if not include_sql:
        return func(), []

    sql_queries = []

    def _wrapper(execute, sql, params, many, context):
        start = perf_counter()
        try:
            return execute(sql, params, many, context)
        finally:
            sql_queries.append(
                {
                    "sql": sql,
                    "params": repr(params) if params is not None else None,
                    "many": many,
                    "duration_ms": round((perf_counter() - start) * 1000, 3),
                }
            )

    with connection.execute_wrapper(_wrapper):
        result = func()

    return result, sql_queries


def _validate_sql_toggle(include_sql):
    if include_sql and not getattr(settings, "DEBUG", False):
        raise ValueError("include_sql is only available when DEBUG=True")


def _add_sql_metadata(payload, include_sql, sql_queries, request_start):
    if include_sql:
        payload["execution_time_ms"] = round((perf_counter() - request_start) * 1000, 3)
        payload["sql_query_count"] = len(sql_queries)
        payload["sql_queries"] = sql_queries
    return payload


@csrf_exempt
def get_display_descriptor(request, resource_id):
    """
    API endpoint to get display descriptor for a resource.

    Usage: GET /api/display-descriptor/<resource_id>/
    Usage: POST /api/display-descriptor/<resource_id>/
    Body: {"config": {...}}  (config is optional)

    Optional query params:
    - descriptor_only=false|0|no|off : include input payload in response (POST only)
    - include_sql=true|1|yes|on : include captured SQL statements and timings
    """
    if request.method not in {"GET", "POST"}:
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        request_start = perf_counter()
        include_sql = _is_truthy(request.GET.get("include_sql"))
        _validate_sql_toggle(include_sql)

        if request.method == "GET":
            descriptor, sql_queries = _execute_with_sql_capture(
                lambda: render_display_descriptor_for_resource(resource_id),
                include_sql=include_sql,
            )
            payload = {"resource_id": resource_id, "display_descriptor": descriptor}
            return JsonResponse(
                _add_sql_metadata(payload, include_sql, sql_queries, request_start)
            )

        data = json.loads(request.body) if request.body else {}
        config = data.get("config")
        descriptor_only = _is_descriptor_only(request.GET.get("descriptor_only"))

        service = DisplayDescriptorService()
        resource_data, sql_queries_data = _execute_with_sql_capture(
            lambda: service.get_resource_data(resource_id, config_data=config),
            include_sql=include_sql,
        )

        render_func = (
            (lambda: service.render_with_config(resource_data, config))
            if config
            else (lambda: service.render(resource_data))
        )
        descriptor, sql_queries_render = _execute_with_sql_capture(
            render_func,
            include_sql=include_sql,
        )

        sql_queries = sql_queries_data + sql_queries_render

        if descriptor_only:
            payload = {"display_descriptor": descriptor}
            return JsonResponse(
                _add_sql_metadata(payload, include_sql, sql_queries, request_start)
            )

        payload = {
            "resource_id": resource_id,
            "input": resource_data,
            "display_descriptor": descriptor,
        }
        return JsonResponse(
            _add_sql_metadata(payload, include_sql, sql_queries, request_start)
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

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
    - include_sql=true|1|yes|on : include captured SQL statements and timings
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        request_start = perf_counter()
        data = json.loads(request.body)
        resource = data.get("resource", {})
        config = data.get("config")
        descriptor_only = _is_descriptor_only(request.GET.get("descriptor_only"))
        include_sql = _is_truthy(request.GET.get("include_sql"))
        _validate_sql_toggle(include_sql)

        # Use provided config or fall back to default
        if config:
            try:
                service = DisplayDescriptorService()
                descriptor, sql_queries = _execute_with_sql_capture(
                    lambda: service.render_with_config(resource, config),
                    include_sql=include_sql,
                )
            except ValueError as e:
                return JsonResponse({"error": f"Invalid config: {str(e)}"}, status=400)
        else:
            descriptor, sql_queries = _execute_with_sql_capture(
                lambda: render_display_descriptor(resource),
                include_sql=include_sql,
            )

        if descriptor_only:
            payload = {"display_descriptor": descriptor}
            return JsonResponse(
                _add_sql_metadata(payload, include_sql, sql_queries, request_start)
            )

        payload = {"input": resource, "display_descriptor": descriptor}
        return JsonResponse(
            _add_sql_metadata(payload, include_sql, sql_queries, request_start)
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
