from django import template
from collections import defaultdict

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Retrieve item from a dictionary."""
    return dictionary.get(key)


@register.filter
def get_length(dictionary):
    """Return the length of the dictionary plus one."""
    return len(dictionary) + 1


@register.filter
def move_key_to_end(dictionary, key):
    """Move the specified key to the end of the dictionary."""
    if key in dictionary:
        value = dictionary.pop(key)
        dictionary[key] = value
    return dictionary


@register.filter
def calculate_total(dictionary):
    """Calculate the total quantity of an item."""
    return sum(dictionary.values())


@register.filter
def calculate_total_by_key(dictionary, key):
    """Calculate the total quantity of an item by key."""
    return sum(order.get(key, 0) for order in dictionary.values())


@register.filter
def calculate_grand_total(dictionary):
    """Calculate the grand total quantity of an item across all teachers."""
    return sum(sum(order.values()) for order in dictionary.values())


@register.filter
def calculate_combined_grand_total(lunch_data, key):
    """Calculate the grand total quantity of an item across all teachers by key."""
    return sum(order.get(key, 0) for orders in lunch_data.values() for order in orders.values())


@register.filter
def make_tuple(value1, value2):
    return (value1, value2)

