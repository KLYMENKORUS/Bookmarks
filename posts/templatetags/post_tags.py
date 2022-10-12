from django import template
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('posts/list.html')
def show_list(count=5):
    list = Post.published.order_by('-publish')[:count]
    return {'list': list}
