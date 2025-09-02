from django.apps import AppConfig
from django.conf import settings

from mariner_proj.utils.monkey_patcher import apply_monkey_patches

from arches.settings_utils import generate_frontend_configuration


class MarinerProjConfig(AppConfig):
    name = "mariner_proj"
    is_arches_application = True

    def ready(self):
        apply_monkey_patches()
        if settings.APP_NAME.lower() == self.name:
            generate_frontend_configuration()
