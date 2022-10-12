from django import template
from ..models import Image

register = template.Library()


@register.simple_tag
def total_images():
    return Image.published.count()


@register.inclusion_tag('images/image_post.html')
def show_latest_images(count=4):
    latest_images = Image.published.order_by('-created')[:count]
    return {'latest_images': latest_images}
