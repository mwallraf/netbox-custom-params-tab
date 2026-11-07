"""Plugin-scoped presentation of prepared, viewer-authorized native values."""
from django import template
from utilities.templatetags.builtins.tags import customfield_value

register = template.Library()


@register.inclusion_tag('netbox_custom_field_profiles/parameter_value.html')
def parameter_value(row):
    """Only accept prepared rows; reference IDs must never be deserialized here."""
    context = {'row': row}
    if row.field.type == 'url' and not row.is_unset and not row.unavailable:
        # Reuse the runtime's configured scheme policy without its text truncation.
        # Reference rows never enter this native formatter or raw-ID lookup.
        context['url_allowed'] = customfield_value(row.field, row.value)['url_allowed']
    return context
