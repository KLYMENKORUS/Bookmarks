from django import template
from ..models import Image

register = template.Library()


@register.simple_tag
def total_images():
    return Image.users_like.all()


@register.inclusion_tag('images/latest_likes.html')
def show_latest_likes(count=2):
    latest_likes = Image.users_like.filter()[:count]
    return {'latest_likes': latest_likes}
