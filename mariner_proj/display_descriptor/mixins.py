from django.db import models
from ..display_descriptor.service import render_display_descriptor


class DisplayDescriptorMixin:
    """
    Mixin for Django models that can generate display descriptors.

    Assumes the model has a method `get_display_descriptor_data()`
    that returns a dict suitable for the display descriptor engine.
    """

    def get_display_descriptor_data(self) -> dict:
        """
        Override this method to return the data dict for display descriptor rendering.

        Should return a dict with keys matching the field names in your config.
        """
        raise NotImplementedError(
            "Subclasses must implement get_display_descriptor_data"
        )

    def get_display_descriptor(self) -> str:
        """
        Get the display descriptor for this instance.
        """
        data = self.get_display_descriptor_data()
        return render_display_descriptor(data) or str(self)

    @property
    def display_descriptor(self) -> str:
        """Property to get display descriptor."""
        return self.get_display_descriptor()

    def __str__(self):
        return self.get_display_descriptor()

    class Meta:
        abstract = True


# Example usage in a model:
"""
class Monument(models.Model, DisplayDescriptorMixin):
    primary_reference_number = models.CharField(max_length=100)
    # ... other fields

    def get_display_descriptor_data(self):
        return {
            "Primary Reference Number": self.primary_reference_number,
            "Monument Name": [
                {"value": name.name, "Monument Name Use Type": name.use_type}
                for name in self.monument_names.all()
            ]
        }
"""
