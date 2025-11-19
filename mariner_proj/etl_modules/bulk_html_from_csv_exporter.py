import csv
from datetime import datetime
from datetime import timedelta
from tempfile import NamedTemporaryFile
from arches.arches.app.utils.data_management.resources.exporter import ResourceExporter
from arches.arches.app.search.search_export import SearchResultsExporter
from arches.arches.app.models import models
from arches.arches.app.models.models import ResourceInstance
from arches.arches.app.models.system_settings import settings
from arches.arches.app.utils.message_contexts import return_message_context
import arches.arches.app.tasks as tasks
import mariner_proj.tasks as proj_tasks


class BulkHTMLExporter:
    def __init__(self, request=None, loadid=None, params=None):
        self.request = request
        self.loadid = loadid
        self.params = params
    
    def get_resourceid_values(self, request=None):
        """
        Reads CSV file and returns all values from the 'resourceid' column
        """
        content = request.FILES.get("file")
        if content.content_type == "text/csv":
            with NamedTemporaryFile(delete=False) as tmp_file:
                for chunk in content.chunks():
                    tmp_file.write(chunk)
                tmp_file.flush()
                tmp_file.seek(0)
                
                with open(tmp_file.name, "r") as f:
                    reader = csv.DictReader(f)
                    resourceid_values = []
                    
                    # Check if 'resourceid' header exists
                    if 'resourceid' not in reader.fieldnames:
                        raise ValueError("Column 'resourceid' not found in CSV headers")
                    
                    # Extract all values from the resourceid column
                    for row in reader:
                        if row['resourceid']:  # Skip empty values
                            resourceid_values.append(row['resourceid'])
                    
                    return resourceid_values
        else:
            raise ValueError("File is not a CSV")
        
    def return_graphs_and_resources(self, resourceids):
        graphs_and_resources = {}
        for resourceid_value in resourceids:
            graph_value = ResourceInstance.objects.filter(id=resourceid_value).values("graph_id").first()
        if graph_value in graphs_and_resources.keys():
            graphs_and_resources[graph_value].append(resourceid_value)
        else:
            graphs_and_resources[graph_value] = [resourceid_value]   
            
        return graphs_and_resources
    
    def return_html_reports_for_resources(self,graph_resource_dict,resourcetotal):
               
        ret = []
        
        for k, v in graph_resource_dict.items():
            graph_id = k
            resources = v
            graph = models.GraphModel.objects.get(pk=graph_id)
            html_exporter = ResourceExporter(format="html")
            ret.append(html_exporter.export(graphid=graph,resourceinstanceids=resources))
            
        return ret
    
    def export_bulk_html_write_zipfile(self, html_reports, search_export_info, resourceids):
        current_user=self.request.user
        search_export_info = models.SearchExportHistory(
            user=current_user,
            numberofinstances=len(resourceids),
            url=None,
        )
        search_export_info.save()
        
        exportid = SearchResultsExporter.write_export_zipfile(html_reports, search_export_info, None)
        
        search_history_obj = models.SearchExportHistory.objects.get(pk=exportid)

        expiration_date = datetime.now() + timedelta(
            seconds=settings.CELERY_SEARCH_EXPORT_EXPIRES
        )
        formatted_expiration_date = expiration_date.strftime("%A, %d %B %Y")
        
        export_name = search_history_obj.get_export_name()

        context = return_message_context(
            greeting=_(
                "Hello,\nYour request to download a set of search results is now ready. You have until {} to access this download, after which time it'll be deleted.".format(
                    formatted_expiration_date
                )
            ),
            closing_text=_("Thank you"),
            email=current_user.email,
            additional_context={
                "link": str(exportid),
                "button_text": _("Download Now"),
                "name": export_name,
                "email_link": str(settings.PUBLIC_SERVER_ADDRESS).rstrip("/")
                + "/files/"
                + str(exportid),
                "username": current_user.first_name or current_user.username,
            },
        )

        return {
            "taskid": self.request.id,
            "msg": _(
                "Your search '{}' is ready for download. You have until {} to access this file, after which we'll automatically remove it.".format(
                    export_name, formatted_expiration_date
                )
            ),
            "notiftype_name": "Search Export Download Ready",
            "context": context,
        }
            
        
    def export_bulk_html_reports(self, request):
  
        resourceids = self.get_resourceid_values(request)
        export_user = request.user.id
        
        if len(resourceids) <= settings.SEARCH_EXPORT_IMMEDIATE_DOWNLOAD_THRESHOLD_HTML_FORMAT:
            
            html_reports = self.return_html_reports_for_resources(self.return_graphs_and_resources(resourceids))
            tasks.notify_completion(export_user,'Search Export Download Ready')

        else:
            
            html_reports = proj_tasks.export_bulk_html_report.apply_async(export_user,resourceids)
            
        

        
    
            
        
            
    
    