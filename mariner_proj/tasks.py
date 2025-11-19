import importlib
import os
import logging
import shutil
from celery import shared_task
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import User
from django.core import management
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.http import HttpRequest
from django.utils.translation import gettext as _
from arches.arches.app.models import models
from arches.arches.app.utils import import_class_from_string
from arches.arches.app.utils.message_contexts import return_message_context
from tempfile import NamedTemporaryFile
from arches.arches.app.search.search_export import SearchResultsExporter
from arches.arches.app.models import models
from arches.arches.app.models.models import ResourceInstance
import arches.arches.app.tasks as tasks


@shared_task

def export_bulk_html_report(self, user, resourceids):
    from mariner_proj.etl_modules import bulk_html_from_csv_exporter
    
    html_exporter_object = bulk_html_from_csv_exporter.BulkHTMLExporter()
    
    html_report_return = html_exporter_object.return_html_reports_for_resources(html_exporter_object.return_graphs_and_resources(resourceids))
    
    html_exporter_object.export_bulk_html_write_zipfile(html_report_return, None, resourceids)
    
    
