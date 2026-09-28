from arches.app.search.components.base import BaseSearchFilter

details = {
    "searchcomponentid": "2f312f1c-7dbb-4112-a364-fd3e954deb8e",
    "name": "LatLong Filter",
    "icon": "fa fa-map-marker",
    "modulename": "latlong-filter.py",
    "classname": "LatLongFilter",
    "type": "latlong-filter-type",
    "componentpath": "views/components/search/latlong-filter",
    "componentname": "latlong-filter",
    "config": {"layoutType": "popup"},
}


class LatLongFilter(BaseSearchFilter):
    def append_dsl(self, search_query_object, **kwargs):
        pass
