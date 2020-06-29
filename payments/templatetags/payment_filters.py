from django import template

register = template.Library()


@register.filter(name='yesno')
def handle_yes_no_from_boolean(value):
    print('************', value)

    if value:
        return 'Yes'

    return 'No'
