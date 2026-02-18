import yaml
import json
from typing import Optional, Dict, Any
from pathlib import Path
from .display_descriptor import DisplayDescriptorEngine
from .models import (
    DisplayDescriptorConfig,
    FieldDefinition,
    Operation,
    RuleDefinition,
    DisplayDescriptorRuleBlock,
)


class DisplayDescriptorService:
    """Service for managing display descriptor configurations and rendering."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self._config_cache: Optional[DisplayDescriptorConfig] = None
        self._engine_cache: Optional[DisplayDescriptorEngine] = None
        self._config_hash: Optional[str] = None

    def _get_default_config_path(self) -> str:
        """Get the default path for display descriptor config."""
        # You can customize this path based on your Django settings
        from django.conf import settings

        base_dir = getattr(settings, "BASE_DIR", Path(__file__).parent.parent)
        return str(Path(base_dir) / "display_descriptor_config.yaml")

    def load_config_from_file(
        self, filepath: Optional[str] = None
    ) -> DisplayDescriptorConfig:
        """Load configuration from a YAML file."""
        filepath = filepath or self.config_path

        try:
            with open(filepath, "r") as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Display descriptor config file not found: {filepath}"
            )
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file: {e}")

        return self._parse_config_data(data)

    def load_config_from_dict(self, data: Dict[str, Any]) -> DisplayDescriptorConfig:
        """Load configuration from a dictionary."""
        return self._parse_config_data(data)

    def load_config_from_json(self, json_str: str) -> DisplayDescriptorConfig:
        """Load configuration from a JSON string."""
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

        return self._parse_config_data(data)

    def _parse_config_data(self, data: Dict[str, Any]) -> DisplayDescriptorConfig:
        """Parse raw config data into DisplayDescriptorConfig."""
        fields_data = data.get("fields", [])
        rules_data = data.get("display_descriptor_rules", [])

        fields = []
        for field_data in fields_data:
            if isinstance(field_data, str):
                fields.append(FieldDefinition(name=field_data))
            elif isinstance(field_data, dict):
                name = field_data.get("name", "")
                subfields = field_data.get("subfields", [])
                fields.append(FieldDefinition(name=name, subfields=subfields))

        rule_blocks = []
        for block_data in rules_data:
            if "rule" not in block_data:
                continue

            rules = []
            for rule_data in block_data["rule"]:
                operations = []
                for op_data in rule_data.get("operations", []):
                    if isinstance(op_data, str):
                        operations.append(Operation(type=op_data))
                    elif isinstance(op_data, dict):
                        operations.append(Operation(**op_data))

                rule = RuleDefinition(
                    name=rule_data["name"],
                    required=rule_data.get("required"),
                    default=rule_data.get("default"),
                    format_when_present=rule_data.get("format_when_present"),
                    format_when_default=rule_data.get("format_when_default"),
                    operations=operations,
                    field_filters=_normalize_field_filters(
                        rule_data.get("field_filters", {})
                    ),
                )
                rules.append(rule)

            format_str = block_data.get("format", "")
            rule_blocks.append(
                DisplayDescriptorRuleBlock(rule=rules, format=format_str)
            )

        return DisplayDescriptorConfig(
            fields=fields, display_descriptor_rules=rule_blocks
        )

    def get_engine(self) -> DisplayDescriptorEngine:
        """Get the cached display descriptor engine."""
        # If no cached engine, load and cache it along with the file checksum.
        config_path = Path(self.config_path)

        current_hash = None
        try:
            current_hash = _compute_file_hash(config_path)
        except FileNotFoundError:
            # If file is missing, fall through and let load_config_from_file raise later
            current_hash = None

        if self._engine_cache is None:
            # initial load
            self._config_cache = self.load_config_from_file()
            self._engine_cache = DisplayDescriptorEngine(self._config_cache)
            self._config_hash = current_hash
            return self._engine_cache

        # If file hash changed since last load, reload config and engine
        if current_hash is not None and self._config_hash != current_hash:
            self._config_cache = self.load_config_from_file()
            self._engine_cache = DisplayDescriptorEngine(self._config_cache)
            self._config_hash = current_hash

        return self._engine_cache

    def render_with_config(
        self, resource: Dict[str, Any], config_data: Dict[str, Any]
    ) -> Optional[str]:
        """Render with an inline config (bypasses file caching)."""
        config = self._parse_config_data(config_data)
        engine = DisplayDescriptorEngine(config)
        return engine.render(resource)

    def render(self, resource: Dict[str, Any]) -> Optional[str]:
        """Render a display descriptor for the given resource."""
        engine = self.get_engine()
        return engine.render(resource)

    def clear_cache(self):
        """Clear the cached config and engine."""
        self._config_cache = None
        self._engine_cache = None


def _normalize_field_filters(raw_filters: dict) -> dict:
    """Normalize field_filters so each value is a list.

    YAML may provide a scalar string (e.g. "Primary|Statutory|Original").
    Ensure consumers always see a list of values.
    """
    if not isinstance(raw_filters, dict):
        return {}

    normalized: dict = {}
    for k, v in raw_filters.items():
        if isinstance(v, str):
            normalized[k] = [v]
        elif isinstance(v, list):
            normalized[k] = v
        else:
            normalized[k] = [v]

    return normalized


def _compute_file_hash(path: Path) -> str:
    """Compute SHA256 hex digest of a file's contents."""
    if not path.exists():
        raise FileNotFoundError(str(path))

    import hashlib

    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# Global service instance
_display_descriptor_service = None


def get_display_descriptor_service() -> DisplayDescriptorService:
    """Get the global display descriptor service instance."""
    global _display_descriptor_service
    if _display_descriptor_service is None:
        _display_descriptor_service = DisplayDescriptorService()
    return _display_descriptor_service


def render_display_descriptor(resource: Dict[str, Any]) -> Optional[str]:
    """Convenience function to render a display descriptor."""
    service = get_display_descriptor_service()
    return service.render(resource)
