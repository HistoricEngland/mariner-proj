import json

from django.conf import settings


def cookie_consent(request=None):
    if request is None:
        return {
            "analytics_cookies": False,
            "accept_all_cookies": False,
        }

    cookie_control = request.COOKIES.get("CookieControl")
    if cookie_control:
        try:
            optional_cookies = json.loads(cookie_control).get("optionalCookies", {})
        except (TypeError, ValueError):
            optional_cookies = {}

        analytics_cookies = optional_cookies.get("analytics") == "accepted"
        return {
            "analytics_cookies": analytics_cookies,
            "accept_all_cookies": analytics_cookies,
        }

    return {
        "analytics_cookies": False,
        "accept_all_cookies": False,
    }


def project_settings(request=None):
    return {
        "proj_settings": {
            "APPLICATIONINSIGHTS_CONNECTION_STRING": getattr(
                settings, "APPLICATIONINSIGHTS_CONNECTION_STRING", ""
            ),
            "APPINSIGHT_SERVICE_NAME": getattr(settings, "APPINSIGHT_SERVICE_NAME", ""),
            # Add any other project-specific settings here as needed
        },
        **cookie_consent(request),
    }
