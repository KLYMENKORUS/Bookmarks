from django import template

register = template.Library()


@register.simple_tag()
def get_companion(user, chat):
    for i in chat.members.all():
        if i != user:
            return i
    return None
