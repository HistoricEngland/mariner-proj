"""
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import inspect


path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

if path not in sys.path:
    sys.path.append(path)

# reverting back to the old style of setting the DJANGO_SETTINGS_MODULE env variable
# refer to the following blog post under the heading "Leaking of process environment variables."
# http://blog.dscpl.com.au/2012/10/requests-running-in-wrong-django.html
os.environ["DJANGO_SETTINGS_MODULE"] = "mariner_proj.settings"


# --- Azure Monitor OpenTelemetry auto-instrumentation ---
from django.conf import settings as djsettings

if getattr(djsettings, "ENABLE_AZURE_MONITORING", True):
    from azure.monitor.opentelemetry import configure_azure_monitor

    connection_string = getattr(
        djsettings, "APPLICATIONINSIGHTS_CONNECTION_STRING", None
    )
    service_name = getattr(djsettings, "APPINSIGHT_SERVICE_NAME", "mariner")
    if not connection_string or not str(connection_string).strip():
        print(
            "[AzureMonitor] Skipping Azure Monitor OpenTelemetry setup: APPLICATIONINSIGHTS_CONNECTION_STRING is not set."
        )
    else:
        instrumentation_options = {
            "django": {"enabled": True},
            "psycopg2": {"enabled": True},
            "requests": {"enabled": True},
            "flask": {"enabled": False},
            "fastapi": {"enabled": False},
        }
        from opentelemetry.sdk.resources import Resource

        resource = Resource.create({"service.name": service_name})
        configure_azure_monitor(
            connection_string=connection_string,
            resource=resource,
            instrumentation_options=instrumentation_options,
            enable_live_metrics=True,
        )
        print("[AzureMonitor] Azure Monitor OpenTelemetry setup complete.")


from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from arches.app.models.system_settings import settings

settings.update_from_db()
