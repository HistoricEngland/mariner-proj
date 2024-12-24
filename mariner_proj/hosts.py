import re
from django_hosts import patterns, host

host_patterns = patterns(
    "",
    host(re.sub(r"_", r"-", r"mariner_proj"), "mariner_proj.urls", name="mariner_proj"),
)
