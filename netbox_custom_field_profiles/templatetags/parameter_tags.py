"""Plugin-scoped presentation of prepared, viewer-authorized native values."""
from django import template

register = template.Library()


@register.inclusion_tag('netbox_custom_field_profiles/parameter_value.html')
def parameter_value(row):
    """Only accept prepared rows; reference IDs must never be deserialized here."""
    return {'row': row}
