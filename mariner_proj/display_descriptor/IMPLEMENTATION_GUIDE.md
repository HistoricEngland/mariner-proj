# Display Descriptor Implementation Guide (Developers)

This document explains what the code currently does at runtime, from API request through data extraction and descriptor rendering.

## TL;DR

The display descriptor implementation has two modes:

1. **In-memory mode**: render a descriptor from a supplied `resource` object (`preview` endpoint).
2. **DB-backed mode**: build `resource` data dynamically from Arches tables (`resource_instances`, `nodes`, `tiles`, `values`) and then render.

The pipeline is:

1. Parse config (`display_descriptor_config.yaml` or inline config)
2. Validate config operations and field topology
3. Resolve field values (either from supplied JSON or DB)
4. Apply rule blocks in order; first successful block wins
5. Return descriptor (optionally with SQL trace metadata in DEBUG)

---

## Code Map

- `display_descriptor/views.py`
  - API request handling
  - Response shaping (`descriptor_only`, SQL tracing)
- `display_descriptor/service.py`
  - Config loading/parsing/caching
  - Dynamic DB extraction for resource fields
  - Validation (missing fields, subfield/parent nodegroup mismatch)
- `display_descriptor/display_descriptor.py`
  - Rule execution engine
  - Field filter logic
  - Operation chain logic
- `display_descriptor/models.py`
  - Dataclasses representing config schema

---

## API Runtime Behavior

### 1) `GET /api/display-descriptor/<resource_id>/`

Flow:

1. Calls `render_display_descriptor_for_resource(resource_id)`
2. Service loads config (cached) and resolves resource data from DB
3. Engine evaluates rule blocks and returns first successful descriptor

Response (default):

```json
{
  "resource_id": "...",
  "display_descriptor": "..."
}
```

Query params:

- `strict_sortorder=true` enforces sortorder consistency checks during DB extraction.

### 2) `POST /api/display-descriptor/<resource_id>/`

Body:

```json
{
  "config": {
    "fields": [...],
    "display_descriptor_rules": [...]
  }
}
```

Flow:

1. If `config` present, service parses that config (no file-cache dependency for schema)
2. Service builds resource data for `<resource_id>` using the supplied or default config fields
3. Engine renders using supplied config (`render_with_config`) or default config (`render`)

Response defaults to descriptor-only, unless `descriptor_only=false`.

Query params:

- `strict_sortorder=true` enforces sortorder consistency checks during DB extraction.

### 3) `POST /api/display-descriptor/preview/`

Body:

```json
{
  "resource": {...},
  "config": {...}
}
```

This mode does **not** pull from DB; it renders directly from provided resource JSON.

`strict_sortorder` is accepted for API consistency but has no effect in preview mode.

---

## SQL Trace Mode (`include_sql`)

Query param: `include_sql=true`

When enabled:

- SQL is captured via Django `connection.execute_wrapper`
- Each query includes `sql`, `params`, `many`, `duration_ms`
- Response includes:
  - `execution_time_ms` (total endpoint time)
  - `sql_query_count`
  - `sql_queries`

Security/operational guard:

- `include_sql` is only allowed when `DEBUG=True`
- Otherwise request returns `400`

---

## Config Parsing and Validation

`DisplayDescriptorService._parse_config_data` transforms raw YAML/JSON into dataclasses:

- `DisplayDescriptorConfig`
- `FieldDefinition`
- `DisplayDescriptorRuleBlock`
- `RuleDefinition`
- `Operation`

`display_descriptor_rules` blocks may omit `rule`; omitted `rule` is normalized to an empty list (`[]`), enabling unconditional fallback blocks such as `{"format": "Unknown"}`.

### Operation validation

- Each operation type is validated against `OperationType` enum
- Unknown operations raise `ValueError`

### Field filter normalization

- `field_filters` values are normalized to lists
- Example: `"Primary|Statutory|Original"` becomes `["Primary|Statutory|Original"]`

---

## DB-backed Resource Data Extraction

Primary entrypoint: `DisplayDescriptorService.get_resource_data(...)`

### Step 1: Resolve graph for resource

- Query `resource_instances` by `resourceinstanceid`
- Read `graph_id`
- If not found: `ValueError("Resource instance not found...")`

### Step 2: Resolve configured field nodes

- Collect field names + subfield names from config
- Query `nodes` for matching names within `graph_id`
- Build `node_map`

Validation at this stage:

1. **All configured field names must exist** in `nodes`
2. **Each subfield must share parent nodegroup**

If either fails: `ValueError` is raised and processing stops.

### Step 3: Group by nodegroup and query tiles

- Fields are grouped by `nodegroup_id`
- For each group, query `tiles` by:
  - `resourceinstance_id`
  - `nodegroup_id`
- Order: `sortorder`, then `tileid`

### Step 4: Extract node values from `tiledata`

Datatype-specific extraction:

- `string`: expects i18n object (`{ "en": {"value": ...} }`), with fallback to first localized value
- `concept`: returns UUID string placeholder initially
- other types: raw value passthrough

Subfield structure handling:

- If field has subfields, each row becomes an object:

```json
{
  "value": "<parent_value>",
  "<Subfield Name>": "<subfield_value>"
}
```

### Step 5: Concept label resolution

- Collect all concept UUIDs found during extraction
- Query `values` once using `valueid__in`
- Replace UUID placeholders with `values.value` labels

### Step 6: Shape result for engine

- Scalar lists with one item are collapsed to scalar
- Fields missing in DB output are defaulted:
  - `None` for simple fields
  - `[]` for fields with subfields

Output is a dictionary keyed by config field names, suitable for the engine.

---

## Rule Engine Behavior

Engine entrypoint: `DisplayDescriptorEngine.render(resource)`

### Rule block execution model

- Iterate `display_descriptor_rules` in order
- For each block, execute each `rule` item
- If required value missing and no default, block fails
- First block that formats successfully wins

### Field filtering behavior

`select_field_value` supports list-of-dict fields with `field_filters`.

Priority filters:

- If filter value contains pipe (`"A|B|C"`), it behaves as ordered priority
- Returns first matching candidate

Simple filters:

- Equality match against allowed values list

### Operation chains

- Operations execute sequentially
- Some operations are string-or-list, some list-only (`unique`, `sort`, `reverse`)
- `combine` converts list to string, affecting downstream operations

---

## Error Handling Semantics

Service raises `ValueError` for predictable user/config/data issues:

- Invalid config operation
- Missing fields in graph
- Subfield nodegroup mismatch
- Missing resource instance
- Sortorder consistency issue when `strict_sortorder=True`

API layer maps these to HTTP `400` responses.

Unexpected runtime errors are returned as HTTP `500`.

---

## Caching and Reload Behavior

Default config mode (`render`):

- Config file checksum (SHA256) is tracked
- If file contents change, config+engine cache is rebuilt on next call

Inline config mode (`render_with_config`):

- Bypasses file cache for rendering
- Still parses and validates operation types

---

## Extensibility Notes

Common extension points:

1. Add operation type:
   - Add enum member in `OperationType`
   - Implement operation function
   - Register handler in `OPERATION_HANDLERS`

2. Add datatype extraction strategy:
   - Extend `_extract_value` in `DisplayDescriptorService`

3. Add stronger ordering policy:
   - Use `strict_sortorder=True`
   - Extend sort validation rules if needed

4. Add additional API-level diagnostics:
   - Extend `_add_sql_metadata` in `views.py`

---

## Practical Adoption Guidance

For teams integrating this feature:

1. Start with `preview` endpoint and static resource payloads.
2. Validate rule behavior and operation ordering.
3. Move to DB-backed endpoint with real `resource_id`.
4. Enable `include_sql=true` in DEBUG to verify query behavior.
5. Lock down production behavior (DEBUG false, no SQL diagnostics).

This approach minimizes risk and makes failures easier to interpret while adopting the system.
