from datetime import datetime
from django import template

register = template.Library()


@register.filter
def to_int(value) -> int:
    return int(value)


@register.filter
def number_to_string(value) -> str:
    integer_number = int(value)
    return "{:,.0f}".format(integer_number)


@register.filter
def lower(value: str) -> str:
    return str.lower(value)


@register.filter
def float_to_string(value):
    return "{:,.1f}".format(value)


@register.filter
def to_ms(date):
    if isinstance(date, datetime):
        milliseconds = int(date.timestamp() * 1000)
        return milliseconds
    else:
        return "Invalid date format"
