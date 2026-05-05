from django import template

register = template.Library()


@register.filter
def dict_value(d, key):
    """Look up key in a dict; returns None if missing or d is not a dict."""
    if isinstance(d, dict):
        return d.get(key)
    return None
