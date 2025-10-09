from django.conf import settings


def project_settings(request=None):
    return {
        "proj_settings": {
            "APPLICATIONINSIGHTS_CONNECTION_STRING": getattr(
                settings, "APPLICATIONINSIGHTS_CONNECTION_STRING", ""
            ),
            "APPINSIGHT_SERVICE_NAME": getattr(settings, "APPINSIGHT_SERVICE_NAME", ""),
            # Add any other project-specific settings here as needed
        }
    }
