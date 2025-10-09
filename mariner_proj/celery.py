from __future__ import absolute_import, unicode_literals
import os
import logging
from celery import Celery
from celery.signals import worker_process_init
import platform

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mariner_proj.settings")

# Configure Azure Monitor first so subsequent instrumentation hooks attach correctly
try:
    logging.getLogger("mariner.telemetry").debug("Starting Celery Azure Monitor setup")
    from mariner_proj.utils.azure_monitoring import setup_azure_monitor

    setup_azure_monitor("celery")
except Exception as _ex:  # pragma: no cover - defensive
    logging.getLogger("mariner.telemetry").warning(
        "Azure Monitor Celery setup skipped: %s", _ex
    )

try:
    from opentelemetry.instrumentation.celery import CeleryInstrumentor  # type: ignore

    @worker_process_init.connect(weak=False)
    def init_celery_tracing(*args, **kwargs):
        CeleryInstrumentor().instrument()
        logging.getLogger("mariner.telemetry").debug("Celery instrumentation attached")

except Exception as _ex:  # pragma: no cover - defensive
    logging.getLogger("mariner.telemetry").warning(
        "Celery OpenTelemetry instrumentation unavailable: %s", _ex
    )

if platform.system().lower() == "windows":
    os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1")

app = Celery("mariner_proj")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
