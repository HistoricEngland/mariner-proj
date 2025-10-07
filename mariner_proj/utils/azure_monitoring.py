"""Centralised Azure Monitor OpenTelemetry configuration.

This module encapsulates repeated logic that was previously duplicated in
`wsgi.py`, `manage.py`, and `celery.py`.

Design goals:
 - Idempotent: safe to call multiple times; subsequent calls no-op.
 - Context-aware: enable only the relevant instrumentation for the runtime.
 - Defensive: never raise exceptions that would block app start; instead log to stdout.
 - Explicit: instrumentation options declared so behaviour is clear during review.

Usage:
    from mariner_proj.utils.azure_monitoring import setup_azure_monitor
    setup_azure_monitor(context="web")  # or "manage", "celery"
"""

from __future__ import annotations

from typing import Literal
import logging

_CONFIGURED = False  # module-level guard
logger = logging.getLogger("mariner.telemetry")


def setup_azure_monitor(context: Literal["web", "manage", "celery"]) -> bool:
    """Configure Azure Monitor OpenTelemetry exporters & instrumentation.

    Parameters
    ----------
    context: One of "web", "manage", or "celery" indicating caller environment.

    Returns
    -------
    bool
        True if configuration succeeded (or was already configured), False if skipped.
    """
    global _CONFIGURED
    if _CONFIGURED:
        logger.debug("Azure Monitor already configured; skipping (context=%s)", context)
        return True

    try:
        # Import inside try so absence of package just results in a skip.
        from azure.monitor.opentelemetry import configure_azure_monitor  # type: ignore
        from opentelemetry.sdk.resources import Resource  # type: ignore
        from django.conf import settings as djsettings  # type: ignore
    except Exception as ex:  # pragma: no cover - defensive
        logger.warning("Azure Monitor dependencies unavailable; skipping setup: %s", ex)
        return False

    try:
        if not getattr(djsettings, "ENABLE_AZURE_MONITORING", True):
            logger.info("Azure Monitor disabled via ENABLE_AZURE_MONITORING=False")
            return False

        connection_string = getattr(
            djsettings, "APPLICATIONINSIGHTS_CONNECTION_STRING", None
        )
        if not connection_string or not str(connection_string).strip():
            logger.warning(
                "APPLICATIONINSIGHTS_CONNECTION_STRING missing; skipping Azure Monitor setup"
            )
            return False

        service_name = getattr(djsettings, "APPINSIGHT_SERVICE_NAME", "mariner")

        # Base instrumentation set common to all contexts.
        instrumentation_options = {
            "psycopg2": {"enabled": True},
            "requests": {"enabled": True},
            # Disable frameworks not in use to reduce overhead / noise
            "flask": {"enabled": False},
            "fastapi": {"enabled": False},
        }

        # Context-specific enablement
        if context in ("web", "manage"):
            instrumentation_options["django"] = {"enabled": True}
            instrumentation_options["celery"] = {"enabled": False}
        elif context == "celery":
            instrumentation_options["django"] = {"enabled": False}
            instrumentation_options["celery"] = {"enabled": True}
        else:  # pragma: no cover - exhaustive guard
            logger.warning(
                "Unknown Azure Monitor context '%s'; using base instrumentation only",
                context,
            )

        resource = Resource.create(
            {
                "service.name": f"{service_name}-{context}",
                "service.instance.id": context,
            }
        )

        configure_azure_monitor(
            connection_string=connection_string,
            resource=resource,
            instrumentation_options=instrumentation_options,
            enable_live_metrics=True,
        )
        _CONFIGURED = True
        logger.info("Azure Monitor OpenTelemetry configured (context=%s)", context)
        return True
    except Exception as ex:  # pragma: no cover - defensive
        logger.error("Azure Monitor setup failed (context=%s): %s", context, ex)
        return False
