# templatetags/cart_extras.py
from django import template

register = template.Library()

@register.filter
def multiply(quantity, price):
    return quantity * price
