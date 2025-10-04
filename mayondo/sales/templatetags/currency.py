from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def ugx(value):
    """
    Format a number as UGX with commas.
    Example: 1000000 -> '1,000,000 UGX'
    """
    try:
        value = float(value)
        return f"{intcomma(int(value))} UGX"
    except (ValueError, TypeError):
        return value
