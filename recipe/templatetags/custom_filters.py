from django import template

register = template.Library()

@register.filter
def split_amount(value):
    return value.split(' ', 1) if ' ' in value else (value, '')
