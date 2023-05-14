from django import template


register = template.Library()


@register.filter('split')
def split(value):
    return value.split('\n')
