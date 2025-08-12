# core/templatetags/form_tags.py
from django import template

register = template.Library()

@register.filter(name='get_field_by_name')
def get_field_by_name(form, field_name):
    """
    Retrieves a bound field from a form instance by its name.
    Usage: {{ form|get_field_by_name:"my_field" }}
    """
    try:
        return form.get(field_name) # Use form.get() which is a safe way to retrieve a field
    except KeyError:
        return None

@register.filter(name='add')
def add(value, arg):
    """
    Adds the arg to the value.
    Usage: {{ value|add:arg }}
    (Note: The built-in 'add' filter does this, but this ensures it's available)
    """
    return value + str(arg)
